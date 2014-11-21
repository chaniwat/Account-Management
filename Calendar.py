import calendar
year = input()
for i in xrange(1, 13):
    c = calendar.TextCalendar(calendar.SUNDAY)
    c.prmonth(year, i)
    print "\n"