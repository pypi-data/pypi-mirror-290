"""Class for a suburb game."""

import random
from typing import TYPE_CHECKING

import networkx as nx
from plotly.express import choropleth

if TYPE_CHECKING:
    from plotly.graph_objects import Figure

    from sydneysuburbs.suburb import Suburb
    from sydneysuburbs.suburb_network import SuburbNetwork


class SuburbGame:
    """Class for a suburb game.

    Attributes:
        suburb_network: Network of suburbs for this game
        start: Starting suburb id
        end: Ending suburb id
        length: Number of suburbs in the shortest path (inclusive of start and end)
        allowable_guesses: Number of allowable guesses (intermediate suburbs)
        all_simple_paths: List of all simple paths between start and end, expanded to
            include the number of extra allowable guesses
        guesses: List of guesses
        guess_scores: List of guess scores
        guesses_remaining: Number of guesses remanining
    """

    suburb_network: "SuburbNetwork"
    start: int
    end: int
    length: int
    allowable_guesses: int
    all_simple_paths: list[list[int]]
    guesses: list[int]
    guess_scores: list[int]
    guesses_remaining: int

    def __init__(
        self,
        suburb_network: "SuburbNetwork",
    ) -> None:
        """Inits the SuburbGame class.

        Args:
            suburb_network: Suburb network object for this game
        """
        self.suburb_network = suburb_network

    def start_game(
        self,
        start: str | int,
        end: str | int,
    ) -> None:
        """Starts a suburb game from the ``start`` suburb to the ``end`` suburb.

        Args:
            start: Starting suburb name or id
            end: Ending suburb name or id

        Raises:
            ValueError: If a suburb cannot be found
        """
        # get start and end suburbs
        if isinstance(start, str):
            start = self.suburb_network.get_suburb_id_by_name(suburb_name=start)

        if isinstance(end, str):
            end = self.suburb_network.get_suburb_id_by_name(suburb_name=end)

        self.start = start
        self.end = end

        # compute shortest path length (number of suburbs from start to end inclusive)
        # note add 1 as this function returns the steps, not suburbs
        self.length = (
            nx.shortest_path_length(
                G=self.suburb_network.graph, source=start, target=end
            )
            + 1
        )

        # initialise guesses remaining (subtract 2 for start and end suburbs)
        self.guesses_remaining = self.length - 2

        # reset guesses and scores
        self.guesses = []
        self.guess_scores = []

        # return allowable number of guesses (https://travle.earth/extra_info)
        if self.length < 6:
            self.allowable_guesses = self.length + 2
        elif self.length < 9:
            self.allowable_guesses = self.length + 3
        elif self.length < 12:
            self.allowable_guesses = self.length + 4
        elif self.length < 15:
            self.allowable_guesses = self.length + 5
        else:
            self.allowable_guesses = self.length + 6

        # generate list of all simple paths
        # calculate cutoff (defined as number of steps = guesses + 1)
        cutoff = self.allowable_guesses + 1
        self.all_simple_paths = list(
            nx.all_simple_paths(
                G=self.suburb_network.graph,
                source=self.start,
                target=self.end,
                cutoff=cutoff,
            )
        )

    def start_random_game(
        self,
        max_length: int,
        min_length: int = 5,
    ) -> None:
        """Starts a game between two random suburbs subject to the length constraints.

        Args:
            max_length: Maximum number of suburbs in the shortest path
            min_length: Minimum number of suburbs in shortest path, defaults to 5

        Raises:
            ValueError: If ``max_length`` is less than ``min_length``
        """
        # check max_length
        if max_length < min_length:
            raise ValueError("max_length must be greater than or equal to min_length.")

        # randomly choose the starting suburb
        start = random.randint(0, len(self.suburb_network.suburbs) - 1)

        # get dict of paths from start that are less than or equal to the max_length
        paths = nx.single_source_shortest_path(
            G=self.suburb_network.graph, source=start, cutoff=max_length - 1
        )

        # get list of possible ends by constraining min_length
        ends = [key for key, val in paths.items() if len(val) >= min_length]

        # pick a random end point
        end = random.choice(ends)

        # start game
        return self.start_game(start=start, end=end)

    def guess(
        self,
        guess: str | int,
    ) -> str:
        """Guess a suburb.

        The guesses are scored as follows:
        - 0 (green) - the guess reduced the guesses remanining
        - 1 (orange) - the guess did not reduce the guesses remaining, however the guess
          is within all_simple_paths (is a suburb that could help get to the destination
          within the allowable number of guesses)
        - 2 (red) - the guess did not reduce the guesses remaining and will not help get
          to the destination within the allowable number of guesses

        Args:
            guess: Guess suburb name or id

        Raises:
            ValueError: If a suburb cannot be found or guess has already been made

        Returns:
            Suburb string
        """
        if isinstance(guess, str):
            guess = self.suburb_network.get_suburb_id_by_name(suburb_name=guess)

        if guess in self.guesses or guess == self.start or guess == self.end:
            raise ValueError(
                "Suburb has already been guessed or is the start or end suburb!"
            )

        # add the guess to the list of guesses
        self.guesses.append(guess)

        # compute guesses remaining:
        # 1) update list of all simple paths (remove current guess if in list)
        # keep track of if the guess was in the list of all simple paths
        found_guess = False

        for p in self.all_simple_paths:
            if guess in p:
                p.remove(guess)
                found_guess = True

        # 2) if guess note found we do not need to update the guesses remaining list
        if not found_guess:
            self.guess_scores.append(2)
            return self.suburb_network.suburbs[guess].name

        # 3) calculate the guesses remaining
        # note we subtract two for the start and end suburbs
        new_guesses_remaining = min([len(p) for p in self.all_simple_paths]) - 2

        # 4) compare new_guesses remaining with old
        # if the guesses remaining is unchanged
        if new_guesses_remaining == self.guesses_remaining:
            self.guess_scores.append(1)
            return self.suburb_network.suburbs[guess].name

        # 5) update guesses remanining and guess score
        self.guesses_remaining = new_guesses_remaining
        self.guess_scores.append(0)

        return self.suburb_network.suburbs[guess].name

    def get_remaining_suburbs(self) -> list["Suburb"]:
        """Gets a list of the suburbs that have not been guessed (or are start, end).

        Returns:
            Remanining suburbs
        """
        start = self.suburb_network.suburbs[self.start]
        end = self.suburb_network.suburbs[self.end]
        guessed_subs = [self.suburb_network.suburbs[guess] for guess in self.guesses]
        taken_subs = [start, end, *guessed_subs]

        return [
            sub for sub in self.suburb_network.suburbs_sorted if sub not in taken_subs
        ]

    def is_game_finished(self) -> bool:
        """Determines if the guesses form a path from the start to the end.

        Returns:
            ``True`` if the game is finished, otherwise ``False``
        """
        return self.guesses_remaining == 0

    def plot_game(
        self,
        finished: bool = False,
    ) -> "Figure":
        """Plots the game state.

        Args:
            finished: If True, plots the entire map as well

        Returns:
            Plotly figure object
        """
        # generate geopandas dataframe of start, end and guesses
        gdf = self.suburb_network.df_gps

        # indices of start, end and guesses
        num_suburbs = len(gdf.index)
        idxs = [self.start, self.end, *self.guesses]

        # add indices of unguessed suburbs if the game is over
        if finished:
            unguessed = [i for i in range(num_suburbs) if i not in idxs]
            idxs = [*idxs, *unguessed]

        # geopandas data frame to be plotted
        game_gdf = gdf.iloc[idxs]

        # generate list of colours
        colours = ["start", "end"]

        for score in self.guess_scores:
            if score == 0:
                colours.append("green")
            elif score == 1:
                colours.append("yellow")
            else:
                colours.append("red")

        # add unguessed suburbs
        if finished:
            colours += ["other"] * len(unguessed)

        fig = choropleth(
            data_frame=game_gdf,
            geojson=game_gdf.geometry,
            locations=game_gdf.index,
            color=colours,
            fitbounds="locations",
            hover_name="suburbname",
            basemap_visible=False,
            color_discrete_map={
                "start": "#5dade2",
                "end": "#a569bd",
                "green": "#58d68d",
                "yellow": "#f4d03f",
                "red": "#e74c3c",
                "other": "rgba(255,0,0,0.1)",
            },
        )
        fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><extra></extra>", showlegend=False
        )
        fig.update_layout(
            geo={"bgcolor": "rgba(0,0,0,0)"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        return fig
