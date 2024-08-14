## 打包

python setup.py sdist

## 本地测试

python setup.py develop

## 上传包

twine upload <dist\包名>  --verbose --username __token__ --password <tokenAPI>