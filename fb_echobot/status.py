from models import Check
def initializing():
	data = "No"
	try:
		p = Check.objects.get_or_create(status=data)
		p.save()
		print "updated"
	except:
		print "failed"

initializing()

