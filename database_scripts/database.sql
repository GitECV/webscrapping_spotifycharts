CREATE DATABASE WebscrappingSpotifyCharts;

USE WebscrappingSpotifyCharts;

CREATE TABLE GlobalDailyChart (
    iIdInsertion INT IDENTITY(1,1) PRIMARY KEY,
    dtDatetime DATETIME,
    sPlaylist NVARCHAR(255),
    sIdSong NVARCHAR(500),
    iChartPosition INT,
    sSongName NVARCHAR(500),
    sArtistName NVARCHAR(500),
    iPeak INT,
    sPrevPosition NVARCHAR(125),
    iStreak INT,
    iStreams INT,
    dtReleaseDate DATETIME,
    dtFirstEntryDate DATETIME,
    iFirstEntryPosition INT,
    iTotalDaysOnChart INT
);
