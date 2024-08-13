﻿import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List
from enum import Enum

class Bibliography:
    """Represents the list of bibliography sources available in the document."""
    
    @property
    def bibliography_style(self) -> str:
        """Gets or sets a string that represents the name of the active style to use for a bibliography."""
        ...
    
    @bibliography_style.setter
    def bibliography_style(self, value: str):
        ...
    
    @property
    def sources(self) -> List[aspose.words.bibliography.Source]:
        """Gets a collection that represents all the sources contained in a bibliography."""
        ...
    
    ...

class Contributor:
    """Represents a bibliography source contributor. Can be either an corporate (an organization) or a list of persons."""
    
    def as_person_collection(self) -> aspose.words.bibliography.PersonCollection:
        """Casts contributor to :class:`PersonCollection`, otherwise returns null."""
        ...
    
    def as_corporate(self) -> aspose.words.bibliography.Corporate:
        """Casts contributor to :class:`Corporate`, otherwise returns null."""
        ...
    
    ...

class ContributorCollection:
    """Represents bibliography source contributors."""
    
    @property
    def artist(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the artist of a source."""
        ...
    
    @artist.setter
    def artist(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def author(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the author of a source."""
        ...
    
    @author.setter
    def author(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def book_author(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the book author of a source."""
        ...
    
    @book_author.setter
    def book_author(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def compiler(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the compiler of a source."""
        ...
    
    @compiler.setter
    def compiler(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def composer(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the composer of a source."""
        ...
    
    @composer.setter
    def composer(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def conductor(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the conductor of a source."""
        ...
    
    @conductor.setter
    def conductor(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def counsel(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the counsel of a source."""
        ...
    
    @counsel.setter
    def counsel(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def director(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the director of a source."""
        ...
    
    @director.setter
    def director(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def editor(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the editor of a source."""
        ...
    
    @editor.setter
    def editor(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def interviewee(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the interviewee of a source."""
        ...
    
    @interviewee.setter
    def interviewee(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def interviewer(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the interviewer of a source."""
        ...
    
    @interviewer.setter
    def interviewer(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def inventor(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the inventor of a source."""
        ...
    
    @inventor.setter
    def inventor(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def performer(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the performer of a source."""
        ...
    
    @performer.setter
    def performer(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def producer(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the producer of a source."""
        ...
    
    @producer.setter
    def producer(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def translator(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the translator of a source."""
        ...
    
    @translator.setter
    def translator(self, value: aspose.words.bibliography.Contributor):
        ...
    
    @property
    def writer(self) -> aspose.words.bibliography.Contributor:
        """Gets or sets the writer of a source."""
        ...
    
    @writer.setter
    def writer(self, value: aspose.words.bibliography.Contributor):
        ...
    
    ...

class Corporate(aspose.words.bibliography.Contributor):
    """Represents a corporate (an organization) bibliography source contributor."""
    
    def __init__(self, name: str):
        """Initialize a new instance of the :class:`Corporate` class.
        
        :param name: The name of an organization."""
        ...
    
    @property
    def name(self) -> str:
        """Gets or sets the name of an organization."""
        ...
    
    @name.setter
    def name(self, value: str):
        ...
    
    ...

class Person:
    """Represents individual (a person) bibliography source contributor."""
    
    def __init__(self, last: str, first: str, middle: str):
        """Initialize a new instance of the :class:`Person` class.
        
        :param last: The last name.
        :param first: The last name.
        :param middle: The last name."""
        ...
    
    @property
    def last(self) -> str:
        """Gets or sets the last name of a person."""
        ...
    
    @last.setter
    def last(self, value: str):
        ...
    
    @property
    def first(self) -> str:
        """Gets or sets the first name of a person."""
        ...
    
    @first.setter
    def first(self, value: str):
        ...
    
    @property
    def middle(self) -> str:
        """Gets or sets the middle name of a person."""
        ...
    
    @middle.setter
    def middle(self, value: str):
        ...
    
    ...

class PersonCollection(aspose.words.bibliography.Contributor):
    """Represents a list of persons who are bibliography source contributors."""
    
    @overload
    def __init__(self):
        """Initialize a new instance of the :class:`PersonCollection` class."""
        ...
    
    @overload
    def __init__(self, persons: Iterable[aspose.words.bibliography.Person]):
        ...
    
    @overload
    def __init__(self, persons: List[aspose.words.bibliography.Person]):
        """Initialize a new instance of the :class:`PersonCollection` class."""
        ...
    
    def __getitem__(self, index: int) -> aspose.words.bibliography.Person:
        """Gets or sets a person at the specified index.
        
        :param index: An index into the collection."""
        ...
    
    def __setitem__(self, index: int, value: aspose.words.bibliography.Person):
        ...
    
    def add(self, person: aspose.words.bibliography.Person) -> None:
        """Adds a :class:`Person` to the collection.
        
        :param person: The person to add to the collection."""
        ...
    
    def remove(self, person: aspose.words.bibliography.Person) -> bool:
        """Removes the person from the collection.
        
        :param person: The person to remove from the collection."""
        ...
    
    def remove_at(self, index: int) -> None:
        """Removes the person at the specified index.
        
        :param index: The zero-based index of the person to remove."""
        ...
    
    def clear(self) -> None:
        """Removes all items from the collection."""
        ...
    
    def contains(self, person: aspose.words.bibliography.Person) -> bool:
        """Determines whether the collection contains a specific person.
        
        :param person: The person to locate in the collection."""
        ...
    
    @property
    def count(self) -> int:
        """Gets the number of persons contained in the collection."""
        ...
    
    ...

class Source:
    """Represents an individual source, such as a book, journal article, or interview."""
    
    def __init__(self, tag: str, source_type: aspose.words.bibliography.SourceType):
        """Initialize a new instance of the :class:`Source` class.
        
        :param tag: The identifying tag name.
        :param source_type: The source type."""
        ...
    
    @property
    def lcid(self) -> str:
        """Gets or sets the locale ID of a source."""
        ...
    
    @lcid.setter
    def lcid(self, value: str):
        ...
    
    @property
    def contributors(self) -> aspose.words.bibliography.ContributorCollection:
        """Gets contributors list (author, editor, writer etc) of a source."""
        ...
    
    @property
    def source_type(self) -> aspose.words.bibliography.SourceType:
        """Gets or sets the source type of a source."""
        ...
    
    @source_type.setter
    def source_type(self, value: aspose.words.bibliography.SourceType):
        ...
    
    @property
    def abbreviated_case_number(self) -> str:
        """Gets or sets the abbreviated case number of a source."""
        ...
    
    @abbreviated_case_number.setter
    def abbreviated_case_number(self, value: str):
        ...
    
    @property
    def album_title(self) -> str:
        """Gets or sets the album title of a source."""
        ...
    
    @album_title.setter
    def album_title(self, value: str):
        ...
    
    @property
    def book_title(self) -> str:
        """Gets or sets the book title of a source."""
        ...
    
    @book_title.setter
    def book_title(self, value: str):
        ...
    
    @property
    def broadcaster(self) -> str:
        """Gets or sets the broadcaster of a source."""
        ...
    
    @broadcaster.setter
    def broadcaster(self, value: str):
        ...
    
    @property
    def broadcast_title(self) -> str:
        """Gets or sets the broadcast title of a source."""
        ...
    
    @broadcast_title.setter
    def broadcast_title(self, value: str):
        ...
    
    @property
    def case_number(self) -> str:
        """Gets or sets the case number of a source."""
        ...
    
    @case_number.setter
    def case_number(self, value: str):
        ...
    
    @property
    def chapter_number(self) -> str:
        """Gets or sets the chapter number of a source."""
        ...
    
    @chapter_number.setter
    def chapter_number(self, value: str):
        ...
    
    @property
    def city(self) -> str:
        """Gets or sets the city of a source."""
        ...
    
    @city.setter
    def city(self, value: str):
        ...
    
    @property
    def comments(self) -> str:
        """Gets or sets the comments of a source."""
        ...
    
    @comments.setter
    def comments(self, value: str):
        ...
    
    @property
    def conference_name(self) -> str:
        """Gets or sets the conference or proceedings name of a source."""
        ...
    
    @conference_name.setter
    def conference_name(self, value: str):
        ...
    
    @property
    def country_or_region(self) -> str:
        """Gets or sets the country or region of a source."""
        ...
    
    @country_or_region.setter
    def country_or_region(self, value: str):
        ...
    
    @property
    def court(self) -> str:
        """Gets or sets the court of a source."""
        ...
    
    @court.setter
    def court(self, value: str):
        ...
    
    @property
    def day(self) -> str:
        """Gets or sets the day of a source."""
        ...
    
    @day.setter
    def day(self, value: str):
        ...
    
    @property
    def day_accessed(self) -> str:
        """Gets or sets the day accessed of a source."""
        ...
    
    @day_accessed.setter
    def day_accessed(self, value: str):
        ...
    
    @property
    def department(self) -> str:
        """Gets or sets the department of a source."""
        ...
    
    @department.setter
    def department(self, value: str):
        ...
    
    @property
    def distributor(self) -> str:
        """Gets or sets the distributor of a source."""
        ...
    
    @distributor.setter
    def distributor(self, value: str):
        ...
    
    @property
    def edition(self) -> str:
        """Gets or sets the editor of a source."""
        ...
    
    @edition.setter
    def edition(self, value: str):
        ...
    
    @property
    def guid(self) -> str:
        """Gets or sets the guid of a source."""
        ...
    
    @guid.setter
    def guid(self, value: str):
        ...
    
    @property
    def institution(self) -> str:
        """Gets or sets the institution of a source."""
        ...
    
    @institution.setter
    def institution(self, value: str):
        ...
    
    @property
    def internet_site_title(self) -> str:
        """Gets or sets the internet site title of a source."""
        ...
    
    @internet_site_title.setter
    def internet_site_title(self, value: str):
        ...
    
    @property
    def issue(self) -> str:
        """Gets or sets the issue of a source."""
        ...
    
    @issue.setter
    def issue(self, value: str):
        ...
    
    @property
    def journal_name(self) -> str:
        """Gets or sets the journal name of a source."""
        ...
    
    @journal_name.setter
    def journal_name(self, value: str):
        ...
    
    @property
    def medium(self) -> str:
        """Gets or sets the medium of a source."""
        ...
    
    @medium.setter
    def medium(self, value: str):
        ...
    
    @property
    def month(self) -> str:
        """Gets or sets the month of a source."""
        ...
    
    @month.setter
    def month(self, value: str):
        ...
    
    @property
    def month_accessed(self) -> str:
        """Gets or sets the month accessed of a source."""
        ...
    
    @month_accessed.setter
    def month_accessed(self, value: str):
        ...
    
    @property
    def number_volumes(self) -> str:
        """Gets or sets the number of volumes of a source."""
        ...
    
    @number_volumes.setter
    def number_volumes(self, value: str):
        ...
    
    @property
    def pages(self) -> str:
        """Gets or sets the pages of a source."""
        ...
    
    @pages.setter
    def pages(self, value: str):
        ...
    
    @property
    def patent_number(self) -> str:
        """Gets or sets the patent number of a source."""
        ...
    
    @patent_number.setter
    def patent_number(self, value: str):
        ...
    
    @property
    def periodical_title(self) -> str:
        """Gets or sets the periodical title of a source."""
        ...
    
    @periodical_title.setter
    def periodical_title(self, value: str):
        ...
    
    @property
    def production_company(self) -> str:
        """Gets or sets the production company of a source."""
        ...
    
    @production_company.setter
    def production_company(self, value: str):
        ...
    
    @property
    def publication_title(self) -> str:
        """Gets or sets the publication title of a source."""
        ...
    
    @publication_title.setter
    def publication_title(self, value: str):
        ...
    
    @property
    def publisher(self) -> str:
        """Gets or sets the publisher of a source."""
        ...
    
    @publisher.setter
    def publisher(self, value: str):
        ...
    
    @property
    def recording_number(self) -> str:
        """Gets or sets the recording number of a source."""
        ...
    
    @recording_number.setter
    def recording_number(self, value: str):
        ...
    
    @property
    def ref_order(self) -> str:
        """Gets or sets the reference order of a source."""
        ...
    
    @ref_order.setter
    def ref_order(self, value: str):
        ...
    
    @property
    def reporter(self) -> str:
        """Gets or sets the reporter of a source."""
        ...
    
    @reporter.setter
    def reporter(self, value: str):
        ...
    
    @property
    def short_title(self) -> str:
        """Gets or sets the short title of a source."""
        ...
    
    @short_title.setter
    def short_title(self, value: str):
        ...
    
    @property
    def standard_number(self) -> str:
        """Gets or sets the standard number of a source."""
        ...
    
    @standard_number.setter
    def standard_number(self, value: str):
        ...
    
    @property
    def state_or_province(self) -> str:
        """Gets or sets the state or province of a source."""
        ...
    
    @state_or_province.setter
    def state_or_province(self, value: str):
        ...
    
    @property
    def station(self) -> str:
        """Gets or sets the station of a source."""
        ...
    
    @station.setter
    def station(self, value: str):
        ...
    
    @property
    def tag(self) -> str:
        """Gets or sets the identifying tag name of a source."""
        ...
    
    @tag.setter
    def tag(self, value: str):
        ...
    
    @property
    def theater(self) -> str:
        """Gets or sets the theater of a source."""
        ...
    
    @theater.setter
    def theater(self, value: str):
        ...
    
    @property
    def thesis_type(self) -> str:
        """Gets or sets the thesis type of a source."""
        ...
    
    @thesis_type.setter
    def thesis_type(self, value: str):
        ...
    
    @property
    def title(self) -> str:
        """Gets or sets the title of a source."""
        ...
    
    @title.setter
    def title(self, value: str):
        ...
    
    @property
    def type(self) -> str:
        """Gets or sets the type of a source."""
        ...
    
    @type.setter
    def type(self, value: str):
        ...
    
    @property
    def url(self) -> str:
        """Gets or sets the url of a source."""
        ...
    
    @url.setter
    def url(self, value: str):
        ...
    
    @property
    def version(self) -> str:
        """Gets or sets the version of a source."""
        ...
    
    @version.setter
    def version(self, value: str):
        ...
    
    @property
    def volume(self) -> str:
        """Gets or sets the volume of a source."""
        ...
    
    @volume.setter
    def volume(self, value: str):
        ...
    
    @property
    def year(self) -> str:
        """Gets or sets the year of a source."""
        ...
    
    @year.setter
    def year(self, value: str):
        ...
    
    @property
    def year_accessed(self) -> str:
        """Gets or sets the year accessed of a source."""
        ...
    
    @year_accessed.setter
    def year_accessed(self, value: str):
        ...
    
    @property
    def doi(self) -> str:
        """Gets or sets the digital object identifier."""
        ...
    
    @doi.setter
    def doi(self, value: str):
        ...
    
    ...

class SourceType(Enum):
    """Represents bibliography source types."""
    
    """Specifies the article in a periodical source."""
    ARTICLE_IN_A_PERIODICAL: int
    
    """Specifies the book source."""
    BOOK: int
    
    """Specifies the book section source."""
    BOOK_SECTION: int
    
    """Specifies the journal article source."""
    JOURNAL_ARTICLE: int
    
    """Specifies the conference proceedings source."""
    CONFERENCE_PROCEEDINGS: int
    
    """Specifies the reporter source."""
    REPORT: int
    
    """Specifies the sound recording source."""
    SOUND_RECORDING: int
    
    """Specifies the performance source."""
    PERFORMANCE: int
    
    """Specifies the art source."""
    ART: int
    
    """Specifies the document from internet site source."""
    DOCUMENT_FROM_INTERNET_SITE: int
    
    """Specifies the internet site source."""
    INTERNET_SITE: int
    
    """Specifies the film source."""
    FILM: int
    
    """Specifies the interview source."""
    INTERVIEW: int
    
    """Specifies the patent source."""
    PATENT: int
    
    """Specifies the electronic source."""
    ELECTRONIC: int
    
    """Specifies the case source."""
    CASE: int
    
    """Specifies the miscellaneous source."""
    MISC: int
    

