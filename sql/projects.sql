create table projects(
    project_id int(11) not null auto_increment primary key,
    project_title varchar(40) not null,
    url varchar(200) not null,

    # The Google Analytics ViewID for this site.
    view_id varchar(50) not null,

    # The first day of the month when Google Analytics was added for this site,
    # e.g. "2017-10-01" for "October 2017".
    start_month date

) ENGINE=InnoDB AUTO_INCREMENT=15239276 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
