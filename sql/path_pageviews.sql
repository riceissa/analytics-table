create table path_pageviews(
    pageviews_id int(11) not null auto_increment primary key,
    project_title varchar(40) not null,

    # The date for which the pageviews are recorded.
    pageviews_date date not null,

    # Use a binary collation to distinguish upper and lower cases
    # https://stackoverflow.com/a/6448861/3422337
    pagepath varchar(500) character set utf8mb4 collate utf8mb4_bin not null,

    pageviews int(8) not null,

    unique key `title_and_date_and_path` (`project_title`, `pageviews_date`, `pagepath`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
