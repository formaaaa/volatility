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
Having established the economic phase that we are in now, we took the daily data for our top3 symbols XAUUSD, EURUSD and
GBPUSD, and checked for 2 and 3 standard deviation moves through this period. Then we extracted the dates when at least
one of these symbols had above the 3 st dev moves, and dates when at least two symbols had a move between 2 and 3 st dev

After that we checked what were the economic news releases during this time and the top market headlines, the
majority of them were in fact due to Central Banks decisions,inflation and jobs data. Almost all of them were profitable
days for us, as the clients were positioned on the opposite side of the move, or made trading decisions, during the day
that resulted in realising a loss.

Since 2020 there were 44 days that met the criteria, for now we excluded 2020, as they were mostly related to pandemic,
and also our data for realised and unrealized profit is not comparable to current figures. So that left us with 31 days,
but we also excluded the day when the war started, as it was by far the biggest gain, and we wanted to focus on events
that happen regularly, not very rarely. So this gives us 30 days, 28 in 2022 and 2 in 2021, 29 of which were
profitable. The avg gain was 4.4M realised and 3.4M in total. Also, these moves were responsible for 16% of realised
profit for the period from 2021, and 24% for the period from 2022.

Using historical data we can conclude that, Excluding the War, based on frequency of 2 and 3 st dev moves:
1. we can expect with 96% probability a move of 4.3M realised profit roughly once per month based on data from 2021
2. we can expect with 96% probability a move of 4.5M realised profit twice a  month taking data from 2022,
so from the time current regime started.

We need to check yet the macro regimes in the past 10 years, how many moves like this we had, and also investigate the
% of time that the markets were trending, and the % of time that markets were ranging, and the PnL in these timeframes,
so we will have a more clear understanding of what to expect if the regime changes to less volatile one.





"""