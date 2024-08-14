## 更新依赖文件

pip freeze | out-file -encoding utf8 requirements.txt

## 打包

python setup.py sdist

## 本地测试

python setup.py develop

## 上传包

twine upload <dist\包名>  --verbose --username __token__ --password <tokenAPI>

## 记录

fix: pycharm终端切换至Command Prompt再执行pip freeze > requirements.txt否则会出现乱码，setup打包失败
