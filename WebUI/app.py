from flask import Flask,render_template, request
import os
from werkzeug.utils import secure_filename
from a1 import infer

app=Flask(__name__)

# 首页，用于上传图片和显示结果
@app.route('/', methods=['GET', 'POST'])
def upload_and_process():
    if request.method == 'POST':
        # 获取上传的图片
        image = request.files.get('image')
        textarea=request.form.get('textarea')
      #   image = request.files['image']
      #   textarea=request.form['textarea']
        filenames = []

        if image and textarea:
            # 使用secure_filename获取安全的文件名
            filename1 = secure_filename(image.filename)
            print(filename1)
            print(textarea)
            # 保存上传的图片到本地
            image.save(os.path.join('static', filename1))
            filenames.append(filename1)
            filenames.append(textarea)
            print(filenames)
            infer(filenames[0],filenames[1])
            # 返回结果页面并展示处理后的图片
            return render_template('index.html', image_path="0016.png")
        elif image:
            filename1 = secure_filename(image.filename)
            print(filename1)
            filename11="C:/Users/86136/Desktop/暑期项目/文字和图像/pythonProject/static/"+filename1
            print(filename11)
            # 保存上传的图片到本地
            image.save(os.path.join('static', filename1))
            # 返回结果页面并展示处理后的图片
            infer(filename11)
            return render_template('index.html', image_path="0017.png")
        elif textarea:
            print(textarea)
            filenames.append(textarea)
            infer(filenames[0])
            # 返回结果页面并展示处理后的图片
            return render_template('index.html',image_path="0018.jpeg")
            # 调用AI模型对图片进行处理（在这里，您需要编写AI模型的代码）
        else:
            return render_template('index.html', aaa="请上传图片或文字")


    return render_template('index.html')


if __name__=="__main__":
   app.run(debug=True)