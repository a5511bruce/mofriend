from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from finger.models import *
# Create your views here.

class NormalUserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()



def home(request):
    post_list = Identification.objects.all()
    if request.method == "POST":
        uf = NormalUserForm(request.POST,request.FILES)
        if uf.is_valid():
            # get the info of the form
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
            # write in database
            normalUser = NormalUser()
            normalUser.username = username
            normalUser.headImg = headImg
            normalUser.save()

            #f=wave.open(request.FILES,"rb")
            f = wave.open("C:\\Users\\User\\PycharmProjects\\mofriend\\upload\\upload\\N001.wav", "rb")
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
                return HttpResponse('上傳成功!!NOT Match')
            else:
                if (sb != rstd):
                    return HttpResponse('上傳成功!!NOT Match')
                else:
                    if (sc != rmean):
                        return HttpResponse('上傳成功!!NOT Match')
                    else:
                        if (sv != rvar):
                            return HttpResponse('上傳成功!!NOT Match')
    else:
        uf = NormalUserForm()
    return render(request, 'home.html', {'uf':uf, 'identification_list': post_list})




