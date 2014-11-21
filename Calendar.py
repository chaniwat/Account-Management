"""Calendar Generator: Take input as the target year, Program will print\
a calendar table from January to December of that target year"""
import calendar
year = input()
for i in xrange(1, 13):
    c = calendar.TextCalendar(calendar.SUNDAY)
    c.prmonth(year, i)
    print "\n"