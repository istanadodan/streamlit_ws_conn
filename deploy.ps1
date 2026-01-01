## Docker image 생성
docker build . -t local-registry:5000/streamlit-ws-app:0.1.0

### Docker image를 local docker registry에 등록
docker push local-registry:5000/streamlit-ws-app:0.1.0

# cd .\k8s
### K8s에 배포
# 배포 제거
kubectl rollout restart deployment streamlit-app -n rag
# kdf .\deployment.yaml
# 배포
# kaf .\deployment.yaml

# cd ..