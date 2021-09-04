from crontab import CronTab

cron = CronTab(user=True)

job = cron.new(command='python updateDB.py')
job.minute.every(5)

cron.write('data/cron_log.txt')