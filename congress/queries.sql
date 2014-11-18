.header OFF
.mode list

/* Query 1 -  Return the statecode, county name and 2010 population of all counties who had a population of over 2,000,000 in 2010. Return the rows in descending order from most populated to least*/
select " ";
select "Query 1";

select c.statecode, c.name, c.population_2010
from counties c
where c.population_2010 > 2000000
order by population_2010 desc;


/* Query 2 -  Return a list of statecodes and the number of counties in that state, ordered from the least number of counties to the most
*/
select " ";
select "Query 2";

select statecode, count(*)
from counties c
group by c.statecode
order by count(*) asc;


/* Query 3  - On average how many counties are there per state (return a single real number) */
select " ";
select "Query 3";

select avg(num_counties)
from
(
    select count(*) as num_counties
    from counties c
    group by c.statecode
);

/* Query 4 - return a count of how many states have more than the average number of counties*/
select " ";
select "Query 4";

select count(num_states)
from
(
    select statecode as num_states
    from counties c
    group by c.statecode
    having count(*) >
    (
        select avg(num_counties)
        from
        (
            select count(*) as num_counties
            from counties c
            group by c.statecode
        )
    )
);

/* Query 5 - Data Cleaning - return the statecodes of states whose 2010 population does not equal the sum of the 2010 populations of their counties*/
select " ";
select "Query 5";
select s.statecode
from states s
where s.population_2010 !=
(
    select sum(c.population_2010)
    from counties c
    where c.statecode = s.statecode
);

/* Query 6 - How many states have at least one senator whose first name is John, Johnny, or Jon? (return a single integer)*/
select " ";
select "Query 6";
select count(*)
from states st
where exists
(
    select *
    from senators se
    where se.statecode = st.statecode and (se.name like 'John%' or se.name like 'Jon%')
);

/*Query 7 - Find all the senators who were born in a year before the year their state was admitted to the union.   For each, output the statecode, year the state was admitted to the union, senator name, and year the senator was born.
Note: in SQLite you can extract the year as an integer using the following: "cast(strftime('%Y',admitted_to_union) as integer)"*/
select " ";
select "Query 7";
select st.statecode, strftime('%Y', st.admitted_to_union), se.name, se.born
from states st, senators se
where st.statecode = se.statecode and se.born < cast(strftime('%Y', st.admitted_to_union) as year);

/* Query 8 - Find all the counties of West Virginia (statecode WV) whose population shrunk between 1950 and 2010, and for each, return the name of the county and the number of people who left during that time (as a positive number).*/
select " ";
select "Query 8";
select c.name, c.population_1950 - c.population_2010
from counties c, states s
where s.statecode = 'WV' and s.statecode = c.statecode and c.population_1950 > c.population_2010;

/*Query 9 - Return the statecode of the state(s) that is (are) home to the most committee chairmen*/
select " ";
select "Query 9";
select st.statecode
from states st
where
(
    select count(*)
    from senators se, committees c
    where c.chairman = se.name and se.statecode = st.statecode
)
=
(
    select max(count)
    from
    (
        select statecode, count(*) as count
        from senators se, committees c
        where c.chairman = se.name
        group by se.statecode
    )
);

/*Query 10 - Return the statecode of the state(s) that are not the home of any committee chairmen*/
select " ";
select "Query 10";
select st.statecode
from states st
where st.statecode not in
(
    select se.statecode
    from senators se, committees c
    where se.name = c.chairman
);

/*Query 11 Find all subcommittes whose chairman is the same as the chairman of its parent committee.  For each, return
the id of the parent committee, the name of the parent committee's chairman, the id of the subcommittee, and name of that subcommittee's chairman*/

select " ";
select "Query 11";
select pc.id, pc.chairman, sc.id, sc.chairman
from committees pc, committees sc
where pc.id = sc.parent_committee and pc.chairman = sc.chairman;

/*Query 12 - For each subcommittee where the subcommittee’s chairman was born in an earlier year than the chairman of its parent committee,  Return the id of the parent committee,  its chairman, the year the chairman was born, the id of the submcommittee, it’s chairman and the year the subcommittee chairman was born.  */
select " ";
select "Query 12";
select pc_id, pc_chairman, pc_born, sc_id, sc_chairman, sc_born
from
(
    select pc.id as pc_id, pc.chairman as pc_chairman, s1.born as pc_born, sc.id as sc_id, sc.chairman as sc_chairman, s2.born as sc_born
    from committees pc, committees sc, senators s1, senators s2
    where sc.parent_committee = pc.id and pc.chairman = s1.name and sc.chairman = s2.name
)
where pc_born > sc_born;
