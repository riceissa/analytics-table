create table path_pageviews(
    pageviews_id int(11) not null auto_increment primary key,
    project_title varchar(40) not null,

    # The date for which the pageviews are recorded.
    pageviews_date date not null,

    pagepath varchar(500) not null,

    pageviews int(8) not null,

    unique key `title_and_date_and_path` (`project_title`, `pageviews_date`, `pagepath`)
) ENGINE=InnoDB AUTO_INCREMENT=15239276 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
