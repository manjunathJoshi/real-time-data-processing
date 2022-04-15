def transform_data(raw_data):
	result = []
	raw_payload = raw_data.tobytes()
	transformed_data = raw_payload.decode('utf-8')
	data_array = transformed_data.split()
	for i in range(0,len(data_array)):
		result.append(len(data_array[i]))
	return result

def file_chunk_generator(file_object,CHUNK_SIZE):
	try:
		while True:
			data = file_object.read(CHUNK_SIZE)
			if not data:
				break
			yield data
	except Exception as e:
		raise Exception(str(e))