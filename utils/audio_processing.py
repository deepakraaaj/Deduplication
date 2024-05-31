import numpy as np
import scipy.io.wavfile
import tempfile

def select_master(cursor, data_format, dimension, length):
    query = "SELECT s3_key FROM master WHERE format=? AND dimension=? AND length>=?"
    res = cursor.execute(query, (str(data_format), dimension, length))
    return res.fetchall()

def insert_master(cursor, user, filename, s3_key, data_format, rate, dimension, length):
    cursor.execute("INSERT INTO master (user, file, s3_key, format, rate, dimension, length) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   (user, filename, s3_key, str(data_format), rate, dimension, length))
    cursor.connection.commit()

def insert_subset(cursor, user, filename, master, rate, start, end):
    cursor.execute("INSERT INTO subset (user, file, master, rate, start, end) VALUES(?, ?, ?, ?, ?, ?)",
                   (user, filename, master, rate, start, end))
    cursor.connection.commit()

def proposed_model(user, filename, path, cursor, s3, S3_BUCKET):
    rate, data = scipy.io.wavfile.read(path)
    dim = data.ndim
    files = select_master(cursor, data.dtype, data.ndim, len(data))
    flag = False

    for file in files:
        s3_key = file[0]
        with tempfile.NamedTemporaryFile() as temp_file:
            s3.download_file(S3_BUCKET, s3_key, temp_file.name)
            master_rate, master_data = scipy.io.wavfile.read(temp_file.name)
            N = len(data)
            possibles = np.where(master_data[:-(N-1)] == data[0])[0]

            for i in possibles:
                if np.all(master_data[i + N - 1] == data[N - 1]):
                    Levels = 10
                    for level in range(1, Levels + 1):
                        if np.all(master_data[i + int(len(data) / 10) * (level - 1) : i + int(len(data) / 10) * level] == data[int(len(data) / 10) * (level - 1) : int(len(data) / 10) * level]):
                            if level == Levels:
                                flag = True
                                start = i
                                end = i + N
                                break
            if flag:
                insert_subset(cursor, user, filename, s3_key, master_rate, start, end)
                break
    
    if not flag:
        s3_key = f'masters/{filename}'
        s3.upload_file(path, S3_BUCKET, s3_key)
        insert_master(cursor, user, filename, s3_key, data.dtype, rate, dim, len(data))
