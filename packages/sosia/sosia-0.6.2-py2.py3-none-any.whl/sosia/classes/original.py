"""Main class for sosia."""

from warnings import warn

from sosia.classes import Scientist
from sosia.processing import find_matches, inform_matches, \
    maybe_add_source_names, search_group_from_sources
from sosia.utils import accepts, custom_print


class Original(Scientist):
    @property
    def matches(self):
        """List of Scopus IDs or list of namedtuples representing matches
        of the original scientist in the treatment year.

        Notes
        -----
        Property is initiated via .find_matches().
        """
        try:
            return self._matches
        except AttributeError:
            return None

    @property
    def search_group(self):
        """The set of authors that might be matches to the scientist.  The
        set contains the intersection of all authors publishing in the
        treatment year as well as authors publishing around the year of first
        publication.  Some authors with too many publications in the
        treatment year and authors having published too early are removed.

        Notes
        -----
        Property is initiated via .define_search_group().
        """
        try:
            return self._search_group
        except AttributeError:
            return None

    @property
    def search_sources(self):
        """The set of sources (journals, books) comparable to the sources
        the scientist published in until the treatment year.
        A source is comparable if it belongs to the scientist's main field
        but not to fields alien to the scientist, and if the types of the
        sources are the same as the types of the sources in the scientist's
        main field where she published in.

        Notes
        -----
        Property is initiated via .define_search_sources().
        """
        try:
            return self._search_sources
        except AttributeError:
            return None

    @search_sources.setter
    @accepts((set, list, tuple))
    def search_sources(self, val):
        self._search_sources = maybe_add_source_names(val, self.source_names)

    def __init__(self, scientist, treatment_year, first_year_margin=2,
                 pub_margin=0.2, cits_margin=0.2, coauth_margin=0.2,
                 affiliations=None, period=None, first_year_search="ID",
                 eids=None, refresh=False, sql_fname=None):
        """Representation of a scientist for whom to find a control scientist.

        Parameters
        ----------
        scientist : str, int or list of str or int
            Scopus Author ID, or list of Scopus Author IDs, of the scientist
            to find a control scientist for.

        treatment_year : str or numeric
            Year in which the comparison takes place.  Control scientist will
            be matched on trends and characteristics of the original
            scientist up to this year.

        first_year_margin : numeric (optional, default=2)
            The left and right margin for year of first publication to match
            possible matches and the scientist on.

        pub_margin : numeric (optional, default=0.2)
            The left and right margin for the number of publications to match
            possible matches and the scientist on.  If the value is a float,
            it is interpreted as percentage of the scientist's number of
            publications and the resulting value is rounded up.  If the value
            is an integer, it is interpreted as fixed number of publications.

        cits_margin : numeric (optional, default=0.2)
            The left and right margin for the number of citations to match
            possible matches and the scientist on.  If the value is a float,
            it is interpreted as percentage of the scientists number of
            publications and the resulting value is rounded up.  If the value
            is an integer, it is interpreted as fixed number of citations.

        coauth_margin : numeric (optional, default=0.2)
            The left and right margin for the number of coauthors to match
            possible matches and the scientist on.  If the value is a float,
            it is interpreted as percentage of the scientists number of
            coauthors and the resulting value is rounded up.  If the value
            is an integer, it is interpreted as fixed number of coauthors.

        affiliations : list (optional, default=None)
            A list of Scopus affiliation IDs.  If provided, sosia conditions
            the match procedure on affiliation with these IDs in the
            year of comparison.

        period: int (optional, default=None)
            An additional period prior to the publication year on which to
            match scientists.
            Note: If the value is larger than the publication range, period
            sets back to None.

        first_year_search: str (optional, default="ID")
            How to determine characteristics of possible control scientists
            in the first year of publication.  Mode "ID" uses Scopus Author
            IDs only.  Mode "name" will select relevant profiles based on
            their surname and first name but only when "period" is not None.
            Select this mode to counter potential incompleteness of
            author profiles.

        eids : list (optional, default=None)
            A list of scopus EIDs of the publications of the scientist you
            want to find a control for.  If it is provided, the scientist
            properties and the control group are set based on this list of
            publications, instead of the list of publications obtained from
            the Scopus Author ID.

        refresh : boolean (optional, default=False)
            Whether to refresh cached results (if they exist) or not.  If int
            is passed, results will be refreshed if they are older than
            that value in number of days.

        sql_fname : str (optional, default=None)
            The path of the SQLite database to connect to.  If None, will use
            the path specified in config.ini.
        """
        # Internal checks
        if not isinstance(first_year_margin, (int, float)):
            raise Exception("Argument first_year_margin must be float or integer.")
        if not isinstance(pub_margin, (int, float)):
            raise Exception("Argument pub_margin must be float or integer.")
        if not isinstance(coauth_margin, (int, float)):
            raise Exception("Argument coauth_margin must be float or integer.")
        if first_year_search not in ("ID", "name"):
            raise Exception("Argument first_year_search must be either ID or name.")
        if first_year_search == "name" and not period:
            first_year_search = "ID"
            text = "Argument first_year_search set to ID: Argument period "\
                   "must not be None"
            warn(text)

        # Variables
        if not isinstance(scientist, list):
            scientist = [scientist]
        self.identifier = [int(auth_id) for auth_id in scientist]
        self.treatment_year = int(treatment_year)
        self.first_year_margin = first_year_margin
        self.pub_margin = pub_margin
        self.cits_margin = cits_margin
        self.coauth_margin = coauth_margin
        self.period = period
        self.first_year_name_search = first_year_search == "name"
        self.eids = eids
        if isinstance(affiliations, (int, str)):
            affiliations = [affiliations]
        if affiliations:
            affiliations = [int(a) for a in affiliations]
        self.search_affiliations = affiliations
        self.refresh = refresh
        self.sql_fname = sql_fname

        # Instantiate superclass to load private variables
        Scientist.__init__(self, self.identifier, treatment_year, refresh=refresh,
                           period=period, sql_fname=self.sql_fname)

    def define_search_group(self, stacked=False, verbose=False, refresh=False):
        """Define search_group.

        Parameters
        ----------
        stacked : bool (optional, default=False)
            Whether to combine searches in few queries or not.  Cached
            files will most likely not be reusable.  Set to True if you
            query in distinct fields or you want to minimize API key usage.

        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.

        refresh : bool (optional, default=False)
            Whether to refresh cached results (if they exist) or not.
        """
        # Checks
        if not self.search_sources:
            text = "No search sources defined.  Please run "\
                   ".define_search_sources() first."
            raise Exception(text)

        # Query journals
        params = {"original": self, "stacked": stacked,
                  "refresh": refresh, "verbose": verbose}
        search_group = search_group_from_sources(**params)

        # Remove own IDs and coauthors
        search_group -= set(self.identifier)
        search_group -= self.coauthors

        # Finalize
        self._search_group = sorted(search_group)
        text = f"Found {len(search_group):,} authors for search_group"
        custom_print(text, verbose)
        return self

    def define_search_sources(self, verbose=False):
        """Define .search_sources.

        Within the list of search sources sosia will search for matching
        scientists.  A search source is of the same main field as
        the original scientist, the same types (journal, conference
        proceeding, etc.), and must not be related to fields alien to the
        original scientist.

        Parameters
        ----------
        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.
        """
        field_df = self.field_source
        info_df = self.source_info
        # Sources in scientist's main field
        mask_same_field = field_df["asjc"] == self.main_field[0]
        same_field = set(field_df[mask_same_field]["source_id"].unique())
        # Types of Scientist's sources
        own_source_ids, _ = zip(*self.sources)
        same_sources = info_df["source_id"].isin(own_source_ids)
        main_types = info_df[same_sources]["type"].unique()
        mask_same_types = info_df["type"].isin(main_types)
        same_type = info_df[mask_same_types]["source_id"].unique()
        # Select source IDs
        selected_ids = same_field.intersection(same_type)
        selected = field_df[field_df["source_id"].isin(selected_ids)].copy()
        grouped = selected.groupby("source_id")["asjc"].unique().to_frame()
        # Deselect sources with alien fields
        fields = set(self.fields)
        no_alien_field = grouped["asjc"].apply(lambda s: len(set(s) - fields) == 0)
        grouped = grouped[no_alien_field].drop(columns="asjc")
        # Add source names
        sources = grouped.join(info_df.set_index("source_id")["title"])
        sources = set(sources.reset_index().itertuples(index=False, name=None))
        # Add own sources
        sources.update(self.sources)
        # Finalize
        self._search_sources = sorted(sources, key=lambda x: x[0])
        text = f"Found {len(sources):,} sources matching main field "\
               f"{self.main_field[0]} and source type(s) {'; '.join(main_types)}"
        custom_print(text, verbose)
        return self

    def find_matches(self, stacked=False, verbose=False, refresh=False):
        """Find matches within search_group based on four criteria:
        1. Started publishing in about the same year
        2. Has about the same number of publications in the treatment year
        3. Has about the same number of coauthors in the treatment year
        4. Has about the same number of citations in the treatment year
        5. Works in the same field as the scientist's main field

        Parameters
        ----------
        stacked : bool (optional, default=False)
            Whether to combine searches in few queries or not.  Cached
            files will most likely not be reusable.  Set to True if you
            query in distinct fields or you want to minimize API key usage.

        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.

        refresh : bool (optional, default=False)
            Whether to refresh cached results (if they exist) or not. If int
            is passed and stacked=False, results will be refreshed if they are
            older than that value in number of days.

        Notes
        -----
        Matches are available through property `.matches`.
        """
        # Checks
        if not self.search_group:
            text = "No search group defined.  Please run "\
                   ".define_search_group() first."
            raise Exception(text)
        if not isinstance(refresh, bool) and stacked:
            refresh = False
            warn("refresh parameter must be boolean when stacked=True.  "
                 "Continuing with refresh=False.")

        # Find matches
        matches = find_matches(self, stacked, verbose, refresh)
        text = f"Found {len(matches):,} author(s) matching all criteria"
        custom_print(text, verbose)
        self._matches = sorted([auth_id for auth_id in matches])

    def inform_matches(self, fields=None, verbose=False, refresh=False):
        """Add information to matches to aid in selection process.

        Parameters
        ----------
        fields : iterable (optional, default=None)
            Which information to provide.  Allowed values are "first_name",
            "surname", "first_year", "num_coauthors", "num_publications",
            "num_citations", "num_coauthors_period", "num_publications_period",
            "num_citations_period", "subjects", "affiliation_country",
            "affiliation_id", "affiliation_name", "affiliation_type",
            "language", "num_cited_refs".  If None, will use all
            available fields.

        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.

        refresh : bool (optional, default=False)
            Whether to refresh cached results (if they exist) or not. If int
            is passed and stacked=False, results will be refreshed if they are
            older than that value in number of days.

        Notes
        -----
        Matches including corresponding information are available through
        property `.matches`.

        Raises
        ------
        ValueError
            If `fields` contains invalid keywords.
        """
        # Checks
        if not self._matches:
            text = "No matches defined.  Please run .find_matches() first."
            raise Exception(text)
        allowed_fields = ["first_name", "surname", "first_year",
                          "num_coauthors", "num_publications", "num_citations",
                          "num_coauthors_period", "num_publications_period",
                          "num_citations_period", "subjects",
                          "affiliation_country", "affiliation_id",
                          "affiliation_name", "affiliation_type", "language",
                          "num_cited_refs"]
        if fields:
            invalid = [x for x in fields if x not in allowed_fields]
            if invalid:
                text = "Parameter fields contains invalid keywords: " +\
                       ", ".join(invalid)
                raise ValueError(text)
        else:
            fields = allowed_fields

        text = f"Providing information for {len(self._matches):,} matches..."
        custom_print(text, verbose)
        matches = inform_matches(self, fields, verbose, refresh)
        self._matches = matches
