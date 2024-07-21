drop table if exists projects;

create table projects(
    project_id int(11) not null auto_increment primary key,
    project_title varchar(40) not null,
    url varchar(200) not null,

    # The Google Analytics ViewID for this site.
    view_id varchar(50),

    # The Google Analytics 4 property ID for this site.
    property_id varchar(50),

    # The date when Google Analytics was added for this site.
    start_date date,

    # The date when Google Analytics 4 was added for this site.
    ga4_start_date date

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into projects(project_title, url, view_id, start_date) values
    ('Cognito Mentoring Wiki','https://info.cognitomentoring.org/','83301583','2014-03-12') /* Not yet switched as it's still on an old version of MediaWiki */
; /* currently missing entries: complexity, galois, graph, linear, machinelearning, noncommutative, ref subwiki */

insert into projects(project_title, url, view_id, property_id, start_date, ga4_start_date) values
    /* Vipul's sites */
    ('BART','https://bart.vipulnaik.com/','151101984','368442001','2017-05-21','2023-06-17')
    ,('Calculus subwiki','https://calculus.subwiki.org/','50145310','385104016','2011-09-05','2023-07-02')
    ,('Cattheory subwiki','https://cattheory.subwiki.org/',NULL,'393073515',NULL,'2024-07-20')
    ,('Cellbio subwiki','https://cellbio.subwiki.org/','51788762','394279673','2011-10-20','2023-07-02')
    ,('Companal subwiki','https://companal.subwiki.org/','11272518','394276112','2008-09-11','2024-07-21')
    ,('Cognito Mentoring','https://cognitomentoring.org/','80278113','387480547','2013-12-21','2023-06-19')
    ,('Commalg subwiki','https://commalg.subwiki.org/','11272366','384945529','2008-09-11','2023-07-02')
    ,('Complexity subwiki','https://complexity.subwiki.org/',NULL,'450913740',NULL,'2024-07-19')
    ,('Contract work for Vipul Naik','https://contractwork.vipulnaik.com/','137051483','361187926','2017-01-02','2023-06-17')
    ,('Demography subwiki','https://demography.subwiki.org/','80270608','391692155','2014-01-26','2023-07-02')
    ,('Devec/Demography data portal','https://devec.vipulnaik.com/','185520433','372907146','2018-11-25','2023-07-02')
    ,('Devec subwiki','https://devec.subwiki.org/','162188096','385039983','2017-10-14','2023-07-02')
    ,('Diffgeom subwiki','https://diffgeom.subwiki.org/','11272486','392397224','2008-09-11','2023-07-02')
    ,('Donations list website','https://donations.vipulnaik.com/','137613209','365946471','2017-01-09','2023-07-02')
    ,('Computing data project', 'https://computingdata.vipulnaik.com/', '194324723', '371137700', '2019-04-28', '2023-06-17')
    ,('Diet Watch', 'https://dietwatch.vipulnaik.com/', '196583289', '386782128', '2019-06-08', '2023-06-17')
    ,('Galois subwiki','https://galois.subwiki.org/',NULL,'450938590',NULL,'2024-07-19')
    ,('Graph subwiki','https://graph.subwiki.org/',NULL,'450946699',NULL,'2024-07-20')
    ,('Groupprops subwiki','https://groupprops.subwiki.org/','8783374','384791175','2008-05-10','2023-07-02')
    ,('Learning subwiki','https://learning.subwiki.org/','80270607','391771379','2014-04-30','2023-07-02')
    ,('Linear subwiki','https://linear.subwiki.org/',NULL,'450893649',NULL,'2024-07-19')
    ,('Machinelearning subwiki','https://machinelearning.subwiki.org/',NULL,'439747074','2024-05-05','2024-05-05')
    ,('Market subwiki','https://market.subwiki.org/','14469598','385616227','2009-01-27','2023-07-02')
    ,('Mech subwiki','https://mech.subwiki.org/','14493100','392273062','2009-01-26','2023-07-02')
    ,('Number subwiki','https://number.subwiki.org/','16064309','391632665','2009-03-18','2024-07-14')
    ,('Offene Grenzen','https://de.openborders.info/','88934216','387480228','2014-07-23','2023-06-19')
    ,('Open Borders: The Case','https://openborders.info/','57510771','386272466','2012-03-16','2023-06-19')
    ,('Topospaces subwiki','https://topospaces.subwiki.org/','11272244','384982525','2008-09-11','2023-07-02')
    ,('Vipul Naik','https://vipulnaik.com/','80266001','387480965','2013-12-18','2023-06-19')
    ,('Wikipedia Views','https://wikipediaviews.org/','88649657','386493527','2014-07-16','2023-07-02')
    /* Issa's sites */
    ,('Content Creation Wiki', 'https://contentcreation.issarice.com/', '156584158', '361374755', '2017-07-01', '2023-06-21')
    ,('Cause Prioritization Wiki', 'https://causeprioritization.org/', '103832319', '386302009', '2014-11-01', '2023-06-21')
    ,('Org Watch', 'https://orgwatch.issarice.com/', '177871658', '315080229', '2018-06-17', '2022-05-14')
    ,('AI Watch','https://aiwatch.issarice.com/', '163268990', '365017328', '2017-10-01', '2023-06-23')
    ,('Issa Rice', 'https://issarice.com/', '104557782', '387112675', '2015-05-01', '2023-06-23')
    ,('Issawiki', 'https://wiki.issarice.com/', '218682322', '364790606', '2020-05-15', '2023-06-23')
    ,('Timelines wiki', 'https://timelines.issarice.com/', '142661718', '364967470', '2017-03-01', '2023-06-25')
;
