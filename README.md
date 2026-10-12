# K8s App Deployment

A React + TypeScript frontend packaged as a container, published to Docker Hub,
and deployed to a single-node K3s cluster on Amazon EC2 by Argo CD.

## Repositories

- This repository contains the app, Kubernetes manifests, Argo CD application,
  deployment guide, and thin GitHub Actions caller workflows.
- [`ci-cd-pipelines`](https://github.com/OWNER/ci-cd-pipelines) contains the
  reusable PR CI and main-branch CD workflows. Replace `OWNER` with your
  GitHub account or organization.

## Quick start

1. Follow [`doc/COMPLETE-HANDS-ON-GUIDE.md`](doc/COMPLETE-HANDS-ON-GUIDE.md) to
   create the Docker Hub repository, EC2 host, K3s cluster, and Argo CD
   application.
2. In `.github/workflows/ci.yml` and `.github/workflows/cd.yml`, replace
   `OWNER` with the GitHub account or organization name. Also replace `OWNER`
   in `argocd/application.yaml`.
3. Add the Docker Hub `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` Actions
   secrets, then push both repositories. A pull request runs CI; after merge,
   CD publishes an immutable image and commits its tag to the Kubernetes
   manifest. Argo CD reads that Git change and deploys it to K3s.

The Docker Hub image repository should be public for unauthenticated pulls by
K3s. No AWS credentials or cluster admin credentials are given to GitHub
Actions.

The first CD release seeds both blue and green Deployments with the same image;
blue initially receives Service traffic. Later releases update the inactive
Deployment and change the Service selector in Git. Argo CD's sync waves apply
the Service switch only after the updated Deployment is healthy.

## Local development

Install Node.js 22.12 or later, then run:

```sh
npm ci
npm test
npm run dev
```

Kubernetes is the deployment/runtime platform; Docker Compose is not part of
this project. If you want to exercise the production container locally without
Compose:

```sh
docker build -t deploylab:local .
docker run --rm -p 8080:8080 deploylab:local
```

Open <http://localhost:8080>. Remove the local image when finished with
`docker image rm deploylab:local`.

## Layout

- `src/` — React + TypeScript frontend.
- `Dockerfile`, `nginx.conf` — unprivileged, multi-stage production image.
- `k8s/base/` — blue/green Deployments and the NodePort Service managed by
  Argo CD.
- `scripts/promote_image.py` — selects the standby color and updates the
  manifest image; unit tests cover initial setup and alternating promotions.
- `argocd/application.yaml` — Argo CD Application pointing at `k8s/base/`.
- `.github/workflows/ci.yml` and `cd.yml` — pull-request CI and main-branch
  CD callers.
- `doc/COMPLETE-HANDS-ON-GUIDE.md` — end-to-end AWS, K3s, Argo CD, CI/CD,
  security, troubleshooting, and cleanup guide.
