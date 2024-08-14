## 更新依赖文件

pip freeze | out-file -encoding utf8 requirements.txt

## 打包

python setup.py sdist

## 本地测试

python setup.py develop

## 上传包

twine upload <dist\包名>  --verbose --username __token__ --password <tokenAPI>