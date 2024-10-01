## independet Sub Query with "Where" keyword and returning result is scaler value 
###### find the movie with the highest rateing
SELECT * FROM smartphone.movies
where score = (select max(score) from smartphone.movies)
###### Find the movie with highest profit(vs order by) 
select * from movies
where (gross - budget) = (select max(gross - budget) from movies)
###### Find how many movies have a rating > the avg of all the movie ratings(Find the 
###### count of above average movies)
select * from movies
where score > (select avg(score) from movies)

select count(*) from movies
where score > (select avg(score) from movies)
######  Find the highest rated movie of 2000
select * from movies
where year = 2000 and score = (select max(score) from movies where year = 2000)
###### Find the highest rated movie among all movies whose number of votes are > 
###### the dataset avg votes
select * from movies where score = (select max(score) from movies 
 where votes > (select avg(votes) from movies))

## Independent Subquery with "Where" keyword and returning result is Row Subquery(One Col Multi Rows)
######  Find all users who never ordered
select * from users where
user_id not in (select distinct(user_id) from orders)
(foreign key relation orders and users tabel)
###### Find all the movies made by top 3 directors(in terms of total gross income)
select * from movies where director in (select director, sum(gross) from movies group by director 
order by sum(gross) desc limit 3)
###### With CTEs(common table expression)
###### Find all the movies made by top 3 directors(in terms of total gross income) 
with top_director as (select director from movies group by director 
                      order by sum(gross) desc limit 3)
select * from movies where director in (select * from top_director)
## independet Sub Query with "Where" keyword and returning result is Table Subquery(Multi Col Multi Row)
###### Find the most profitable movie of each year
select * from movies where (year, gross-budget) in 
(select year,max(gross-budget) from movies group by year)
######  Find the highest rated movie of each genre votes cutoff of 25000 
select * from movies where
(genre, score) in (select genre, max(score) from movies where votes > 25000
					group by genre)
and votes > 25000
###### Find the highest grossing movies of top 5 actor/director combo in terms of 
###### total gross income
select * from movies where (star,director,gross) in (select star, director, max(gross) from movies
                                                     group by star, director order by sum(gross) 
                                                     desc limit 5)
###### With CTEs(common table expression)
with top_duos as (select star, director, max(gross) from movies
                  group by star, director order by sum(gross) 
                  desc limit 5)
select * from movies where (star,director,gross) in (select * from top_duos)

## Correlated Subquery with "Where" keyword and returning result is scaler value 
###### Find all the movies that have a rating higher than the average 
###### rating of movies in the same genre.[Animation]
select * from movies m1
where score > (select avg(score) from movies m2 where m2.genre = m1.genre)
###### Find the favorite food of each customer.
with fav_food as (select t2.user_id, t1.name, t4.f_name, count(*) as frequency from users t1
                  join orders t2 on t1.user_id = t2.user_id
				  join order_details t3 on t2.order_id = t3.order_id
                  join food t4 on t3.f_id = t4.f_id 
                  group by t2.user_id,t3.f_id,t1.name, t4.f_name)
select * from fav_food f1
where frequency = (select max(frequency) 
                    from fav_food f2 where
                    f2.user_id = f1.user_id)

## independet Sub Query with "Select" keyword and returning result is scaler value
###### Get the percentage of votes for each movie compared to the total number of 
###### votes.
select name, (votes/(select sum(votes) from movies))*100 from movies
## Correlated Subquery with "Select" keyword and returning result is scaler value 
###### Display all movie names ,genre, score and avg(score) of genre
select name,genre,score, (select avg(score) from movies m2 where m2.genre = m1.genre)
from movies m1
## independet Sub Query with "from" keyword and returning result is Table Subquery(Multi Col Multi Row)
##### Display average rating of all the restaurants
select r_name, avg_rating
from (select r_id, avg(restaurant_rating) as "avg_rating"
       from orders group by r_id) t1 join restaurants t2
       on t1.r_id = t2.r_id
## independet Sub Query with "Having" keyword and returning result is scaler value
###### Find genres having avg score > avg score of all the movies
select genre, avg(score) from movies
group by genre having avg(score) > (select avg(score) from movies)

## Sub Query with "insert" 
###### Populate a already created loyal_customers table with records of only 
###### those customers who have ordered food more than 3 times
insert into loyal_users (user_id, name)
select t1.user_id, name from orders t1 join users t2
on t1.user_id = t2.user_id group by t1.user_id, name
having count(*) > 3
## Sub Query with "Delete"
###### Delete all the customers record who have never ordered.
delete from users where user_id in (select user_id from users where user_id not in
(select distinct(user_id) from orders))
## Sub Query with "update"
###### Populate the money col of loyal_cutomer table using the orders table. 
###### Provide a 10% app money to all customers based on their order value
update loyal_users
set money = (select sum(amount) from orders where orders.user_id = loyal_users.user_id)