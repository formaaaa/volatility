"""
Control exposure risk, measure client risk behavior on all macroeconomic conditions. Introduce trading condition changes
based on historical impact on main company metrics.

Projection of certain market regime periodical frequency Forecasts of trading profits and distribution through for at
least of 1 year. Ongoing client risk level measurement according to the projections.

KR1: Transparent report on trading market conditions based on changing macroeconomic situation. Overlay with clients
behaviour and their profitability. Aimed at forecasting company's results, and their seasonality / periodicity.
KR2: Creating metrics and workflows for ongoing macro regime surveillance, detecting potential turning points and
amending trading conditions.
KR3: Measuring the accuracy of the built models, and the effect it has on our ability to forecast the future cash flows
and mitigate clients risks.
=======================================================================================================================
What we did for now is we checked the macroeconomic situation, and tried to establish what is the current
financial markets phase. As we have PnL results dating back to 2020 in our databases, we focused on those years. We plan
to investigate the prior years and extrapolate current results on those years as well.
(show VIX, GVZ, ES1!)
2020 - was a very volatile year due to pandemic, and depression like economic indicators, as we can see the VIX spiked
        to values way above the 30 level, and stayed above 20 for the remainder of the year, GVZ so gold volatility was
        also elevated at that time
2021 - in 2021 the volatility was more subdued, with VIX and GVZ spending most of the year below the 20 level. Markets
        participants were focusing on big rebound in economic activity after the economies were reopened, and we had
        accelerating GDP and inflation prints
2022 - was again more volatile with VIX ranging between 20 and 30 level, and GVZ especially in the 1st part of the year
        oscillating around 20 level.
(show FEDFUNDS)
        The FED Funds rate started increasing in Q1 of 2022, and economic predictive
        models started to foresee decelerating economic activity. At first there were stagflation fears, that in 2nd
        part of the year switched to recession fears. This is the current regime that we are in now. Markets are
        focusing mostly on Central Banks decisions, reports and speeches from members, inflation data and economic
        activity. These periods of time are characterized by elevated volatility, strong dollar, and more coppy markets
        in result.
======================================================================================================================
In an attempt to forecast the clients PnL we took the daily data for our top3 symbols XAUUSD, EURUSD and
GBPUSD, and checked for above 2 standard deviation daily moves and their frequency. Then we extracted the dates when at
least one of these symbols had above the 2 st dev move.

After that we checked what were the economic news releases during this time and the top market headlines, the
majority of them involved Central Banks interest rates decisions and speeches, or there
were inflation and jobs data releases. Almost all of them were profitable days for us.

Since 2021 there were 50 days that met the criteria. We excluded the day when the war started, as it was by
far the biggest gain, and we wanted to focus on events that could happen regularly. So that left us with 49 days,
21 in 2021 and 28 in 2022. Only 2 of those days were unprofitable for us and the max profit for clients barely exceeded
400k. The avg gain was 3.7M realised for 2021 and 4.5M for 2022. If we didn't exclude 24th of February, the average gain
would be 5.7M in 2022. Also, these moves were responsible for approximately 25% of realised profit during these two
years.

As for 2020, we had 61 days like this, 58 of them were profitable, and the average profit was almost 700k. However,
our figures for this period cannot be directly compared with current values, as the client's exposure at that time
was few times smaller.

Using this historical data we can conclude for now that, based on frequency of at least 2 st dev moves:
1. we can expect a market move that will result in client's realised losses of 4.2M on average roughly twice per month
1a. as for 2021 statistically it was 3 moves every 2 months, averaging 3.7M
1b. as for 2022 statistically it was 2 moves every 1 month, averaging 4.5M

We also checked for 2 st dev moves in prior years, dating back to 2016, and found out that on average they were
happening 37 times a year. So, our expectation of 2 moves per month is not exaggerated.

What we plan to do next, is to research the price trends of major instruments, and figure out how the clients are doing
when the markets are trending, and how do they fare when the markets are ranging, without clear trend in place.
And combine the two approaches.


/
The difference between the two years, can be attributed to much lower volatility on markets in 2021 than 2022
/




"""