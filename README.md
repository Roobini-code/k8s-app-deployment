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

1. Follow [`doc/COMPLETE-HANDS-ON-GUIDE.md`](doc/COMPLETE-HANDS-ON-GUIDE.md)
   in order; it walks through the repositories, Docker Hub, EC2/K3s/Argo CD,
   stable Elastic IP, DNS, cert-manager, and first deployment.
2. In `.github/workflows/ci.yml` and `.github/workflows/cd.yml`, replace
   `OWNER` with the GitHub account or organization name. Also replace `OWNER`
   in `argocd/application.yaml`.
3. Replace `app.example.com` in `k8s/base/ingress.yaml` with your domain and
   `REPLACE-WITH-YOUR-EMAIL` in `k8s/base/cluster-issuer.yaml`. Follow the guide
   in order: publish the initial image, then apply the Argo CD Application.
4. Add the Docker Hub `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` Actions
   secrets, then push both repositories. Merge a qualifying app change to
   trigger the first CD image publish. The guide then has you install
   cert-manager, verify DNS, and apply the Argo CD Application. Subsequent
   merges publish immutable images and update Git for Argo CD to deploy.

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
- `k8s/base/` — blue/green Deployments, private ClusterIP Service, Traefik
  Ingress, HTTPS redirect middleware, and cert-manager ClusterIssuer managed
  by Argo CD.
- `scripts/promote_image.py` — selects the standby color and updates the
  manifest image; unit tests cover initial setup and alternating promotions.
- `argocd/application.yaml` — Argo CD Application pointing at `k8s/base/`.
- `.github/workflows/ci.yml` and `cd.yml` — pull-request CI and main-branch
  CD callers.
- `doc/COMPLETE-HANDS-ON-GUIDE.md` — end-to-end AWS, K3s, Argo CD, CI/CD,
  security, troubleshooting, and cleanup guide.
