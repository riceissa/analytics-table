drop table if exists projects;

create table projects(
    project_id int(11) not null auto_increment primary key,
    project_title varchar(40) not null,
    url varchar(200) not null,

    # The Google Analytics ViewID for this site.
    view_id varchar(50) not null,

    # The date when Google Analytics was added for this site.
    start_date date

) ENGINE=InnoDB AUTO_INCREMENT=15239276 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into projects(project_title, url, view_id, start_date) values
    ('Cause Prioritization Wiki', 'https://causeprioritization.org/', '103832319', '2014-11-01')
    ,('AI Watch','https://aiwatch.issarice.com/', '163268990', '2017-10-01')
    ,('Org Watch', 'https://orgwatch.issarice.com/', '177871658', '2018-06-17')
    ,('Timelines Wiki', 'https://timelines.issarice.com/', '142661718', '2017-03-01')
;
