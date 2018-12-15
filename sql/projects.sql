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
    ,('BART','https://bart.vipulnaik.com/','151101984','2017-05-21')
    ,('Calculus subwiki','https://calculus.subwiki.org/','50145310','2011-09-05')
    ,('Cellbio subwiki','https://cellbio.subwiki.org/','51788762','2011-10-20')
    ,('Cognito Mentoring','https://cognitomentoring.org/','80278113','2013-12-21')
    ,('Commalg subwiki','https://commalg.subwiki.org/','11272366','2008-09-11')
    ,('Companal subwiki','https://companal.subwiki.org/','11272518','2008-09-11')
    ,('Contract work for Vipul Naik','https://contractwork.vipulnaik.com/','137051483','2017-01-02')
    ,('Offene Grenzen','https://de.openborders.info/','88934216','2014-07-23')
    ,('Demography subwiki','https://demography.subwiki.org/','80270608','2014-01-26')
    ,('Devec subwiki','https://devec.subwiki.org/','162188096','2017-10-14')
    ,('Devec/Demography data portal','https://devec.vipulnaik.com/','185520433','2018-11-25')
    ,('Diffgeom subwiki','https://diffgeom.subwiki.org/','11272486','2008-09-11')
    ,('Donations list website','https://donations.vipulnaik.com/','137613209','2017-01-09')
    ,('Groupprops subwiki','https://groupprops.subwiki.org/','8783374','2008-05-10')
;
