with p as (
  select date_trunc('week', sent_at)::date wk, responder, outcome from pings
), pw as (
  select wk, count(*) pings,
    count(*) filter (where outcome in ('taken','turned down')) answered,
    count(*) filter (where outcome = 'taken') taken,
    count(*) filter (where outcome = 'missed') missed,
    count(*) filter (where responder in ('Vesper','The Undertow','Farlight','Meteor Mite')) quiet_four_pings
  from p group by wk
), cw as (
  select date_trunc('week', c.happened_at)::date wk, count(*) callouts,
    count(*) filter (where exists (
      select 1 from pings x where x.callout_number = c.callout_number and x.outcome = 'taken')) filled
  from callouts c group by 1
), tw as (
  select date_trunc('week', filed_at)::date wk,
    count(*) filter (where subject ~* '(hardly anything for|nothing coming through|much quieter|still very quiet|has not gone off|still on the list|asked me to pass this on)') no_pings_tickets,
    count(*) filter (where subject ~* '(vanished before|moved on|gone before|lost one|and (he|she) missed it|missed one while)') gone_tickets,
    count(*) all_tickets
  from support_tickets group by 1
), days as (
  select date_trunc('week', happened_at)::date wk, count(distinct happened_at::date) days_with_data
  from callouts group by 1
)
select cw.wk week_start, days.days_with_data, cw.callouts, cw.filled,
  pw.pings, pw.answered, pw.taken, pw.missed, pw.quiet_four_pings,
  coalesce(tw.no_pings_tickets, 0) no_pings_tickets,
  coalesce(tw.gone_tickets, 0) gone_tickets,
  coalesce(tw.all_tickets, 0) all_tickets
from cw left join pw using (wk) left join tw using (wk) left join days using (wk)
order by 1
