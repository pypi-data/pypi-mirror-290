# 安装相关依赖



## 打包

python setup.py sdist

## 本地测试

python setup.py develop

## 上传包

twine upload <dist\包名>  --verbose --username __token__ --password <tokenAPI>



## loginfo

`0.0.2`：修复通过requirements.txt安装依赖包找不到本文件的问题