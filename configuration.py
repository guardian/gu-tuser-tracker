from models import Configuration

def lookup(key):
	results = Configuration.query(Configuration.key == key)

	if not results.iter().has_next():
		return None

	key_value = results.iter().next().value

	return key_value	