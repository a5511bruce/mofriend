from __future__ import unicode_literals
from django.db import models
import os
import wave
import numpy as np
import pymysql


class Identification(models.Model):
    num = models.CharField(max_length=100)
    avg = models.CharField(max_length=100)
    std = models.CharField(max_length=100)
    mean = models.CharField(max_length=100)
    var = models.CharField(max_length=100)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num
    class Meta:
        db_table = "identification"



class NormalUser(models.Model):
    username = models.CharField(max_length=30)
    headImg = models.FileField(upload_to='./upload')

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['username']


class memory():
    def fp_compare(a):

        f = wave.open(a, "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        str_data = f.readframes(nframes)
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data.shape = -1, sampwidth
        wave_data = wave_data.T
        f.close()
        frames = 40
        block = []
        fft_blocks = []
        high_point = []
        sa = int
        sb = int
        sc = int
        sv = int
        blocks_size = int(framerate / frames)  # block_size为每一块的frame数量

        blocks_num = int(nframes / blocks_size)  # 将音频分块的数量

        # s_point.append(a,b,c,d)
        for i in range(0, len(wave_data[0]) - blocks_size, blocks_size):
            block.append(wave_data[0][i:i + blocks_size])
            fft_blocks.append(np.abs(np.fft.fft(wave_data[0][i:i + blocks_size])))
            high_point.append((np.argmax(fft_blocks[-1][:40]),
                               np.argmax(fft_blocks[-1][40:80]) + 40,
                               np.argmax(fft_blocks[-1][80:120]) + 80,
                               np.argmax(fft_blocks[-1][120:180]) + 120))
        sa = int(np.average(high_point))
        sb = int(np.std(high_point))
        sc = int(np.mean(high_point))
        sv = int(np.var(high_point))

        conn = pymysql.connect("localhost", "root", "a5511bruce", "sd")
        cur = conn.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cur.execute("SELECT avg  FROM test2")
        ravg = cur.fetchone()
        cur.execute("SELECT std  FROM test2")
        rstd = cur.fetchone()
        cur.execute("SELECT mean  FROM test2")
        rmean = cur.fetchone()
        cur.execute("SELECT var  FROM test2")
        rvar = cur.fetchone()
        cur.execute("INSERT  INTO  test2(num,avg,std,mean,var)   VALUES( 'lb2',%s , %s,%s,%s )", (sa, sb, sc, sv))
        conn.commit()
        cur.close()
        conn.close()

        result = int

        if (sa != ravg):
            result = 'NOT match!!'
            print(result)
        else:
            if (sb != rstd):
                result = 'NOT match!!'
                print(result)
            else:
                if (sc != rmean):
                    result = 'NOT match!!'
                    print(result)
                else:
                    if (sv != rvar):
                        result = 'NOT match!!'
                        print(result)
                    else:
                        result = 'MATCH!!'
                        print(result)


if __name__ == '__main__':
    s = memory
    s.fp_compare("C:\\Users\\User\\PycharmProjects\\mofriend\\upload\\upload\\N001.wav")