# Name: Kalvin Lee
# Class: ECON 481
# Problem Set 6

# Exercise 0
    # returns link to solution file on github
def github() -> str:
    return "https://github.com/kalvinlee/ECON481/blob/main/problemset6.py"

# Exercise 1
    # takes no arguments and returns a string containing a SQL query that can be run against the
    # auctions database, outputting a table that has two columns: itemId and std, only including 
    # bids for which the unbiased standard deviation can be calculated which follows the
    # equation s={\sqrt {\frac {\sum _{i=1}^{n}(x_{i}-{\overline {x}})^{2}}{n-1}}}
def std() -> str:
    q = """
        /* chooses itemid and std calc for output, subquery helps filter and calculate before
            going to std calculation, followed by more filtering sorted by itemid */
        select itemid,
        sqrt(sum((bidAmount - avg_amount) * (bidAmount - avg_amount)) / (count - 1)) as std
        from (
            select itemid, bidAmount,
                avg(bidAmount) over (partition by itemid) as avg_amount,
                count(bidAmount) over (partition by itemid) as count
            from bids
            where bidAmount is not null
        )
        where count > 1
        group by itemid
        """
    return q

# Exercise 2
    # takes no arguments and returns a string containing a SQL query that can be run against the
    # auctions database, that outputs a table wil four columns of bidderName, total_spend, total_bids
    # spend_frac
def bidder_spend_frac() -> str:
    q = """
    /* chooses the bidderName, spending, bids, and spend fraction to output, subquery helps
        by choosing which information is valuable for the output, sorted by bidderName*/
    select 
        bidderName,
        sum(case when highBidderName = bidderName then bidAmount else 0 end) as total_spend,
        sum(max) as total_bids,
        sum(case when highBidderName = bidderName then bidAmount else 0 end) / sum(max) as spend_frac
    from (
        select bidderName, itemid, highBidderName, bidAmount, max(bidAmount) as max
        from bids
        group by bidderName, itemid
    )
    group by bidderName;
    """
    return q

# Exercise 3
    # takes no arguments and returns a string containing a SQL query that can be run against the
    # auctions database, that outputs a table that has one column, freq, which represents the fraction
    # of bids that are exactly the minimum bid increment above the previous high bid, excluding items
    # where isBuyNowUsed = 1
def min_increment_freq() -> str:
    q = """
    /* chooses the amount of times the next bid = bidIncrement by joining together the bids 
        items table, subquery helps calculate and determine previous bid, followed by 
        more filtering */
    select sum(case when b.bidAmount - p.prevbid = i.bidIncrement then 1 else 0 end) / count(*) as freq
    from bids as b
    inner join items as i on b.itemId = i.itemId
    inner join (
        select itemId, bidTime, lag(bidAmount) over (partition by itemId order by bidTime) as prevbid
        from bids
    ) as p on b.itemId = p.itemId and b.bidTime = p.bidTime
    where i.isBuyNowUsed != 1;
    """
    return q

# Exercise 4
from sqlalchemy import func, distinct
    # takes no arguments, and returns a string containing a SQL query that can be run against the
    # auctions database that outputs a table that has two columns, timestamp_bin: normalize the
    # bid timestamp and classify it as one of ten bins. ex: 1 corresponds to 0-0.1, 2 to 0.1-0.2 etc.
    # and win_perc: the frequency with which a bid placed with this timestamp bin won the auction
def win_perc_by_timestamp() -> str:
    q = """
    /* stores auction info */
    with a as (
        select itemid, starttime, endtime
        from items
    ), 
    /* figures out the timestamp_bin and which bin it belongs in */
    time as (
        select b.itemid, 
            cast(((julianday(a.endtime) - julianday(b.bidtime)) / 
                (julianday(a.endtime) - julianday(a.starttime)) * 10) + 1 as int) as timestamp_bin,
            max(b.bidAmount) over (partition by b.itemid) as max
        from bids as b
        inner join items as a on b.itemid = a.itemid
    ),
    /* counts the number of items are within each bin */
    win as (
        select time.timestamp_bin, 
        count(distinct b.itemid) as win_count
        from time
        inner join bids as b on time.itemid = b.itemid
                            and time.max = b.bidAmount
        inner join a on b.itemid = a.itemid
        where cast(((julianday(a.endtime) - julianday(b.bidtime)) / 
                   (julianday(a.endtime) - julianday(a.starttime)) * 10) + 1 as int) = time.timestamp_bin
        group by time.timestamp_bin
    )
    /* outputs the bins and the winning percentage from within each bin*/
    select timestamp_bin,
        win_count * 1.0 / (select sum(win_count) from win) as win_perc
    from win
    group by timestamp_bin
    order by timestamp_bin;
    """
    return q