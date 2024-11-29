# Technical case study

## Part 1 - Basic usage

### Requirements

The code has been tested with Python > 3.13.

To install the requirements (`virtualenv` is advised):
```
$ pip install -r requirements.txt
```

To run the tests:

```
$ python -m unittest discover -s src/tests
```

To run the command line 

```
$ python cli.py --help
$ ./cli.py --help
```

With Python 3 and requirements installed:

```
$ ./cli.py -u https://news.ycombinator.com -o stdout
[...]
https://news.ycombinator.com/newsfaq.html
https://news.ycombinator.com/lists
https://news.ycombinator.com/security.html
```

```
$ ./cli.py -u https://news.ycombinator.com -o json | jq 
{
  "https://news.ycombinator.com": [
    "",
    "/news",
    "/newest",
    "/front",
    "/newcomments",
    "/ask",
    [...]
  ]
}
```

## Part 2 - Docker and Kubernetes

Image is published on GitHub container registry based on the `Dockerfile` at root level:

```
$ docker run ghcr.io/paulden/tech-case-study:main -u https://news.ycombinator.com -o stdout
[...]
https://news.ycombinator.com/newsfaq.html
https://news.ycombinator.com/lists
https://news.ycombinator.com/security.html
```

In `deploy/manifests`, there is a `Deployment` to run the image on Kubernetes if the namespace has been created.

```
$ kubectl apply -f deployment.yaml
deployment.apps/url-extractor created
$ kubectl get po
NAME                             READY   STATUS        RESTARTS   AGE
url-extractor-76fc7859f8-45662   1/1     Running       0          5s
$ kubectl logs -f url-extractor-76fc7859f8-45662
[...]
https://news.ycombinator.com/newsfaq.html
https://news.ycombinator.com/lists
https://news.ycombinator.com/security.html
```

### TODO

The Kubernetes part is obviously very basic with a simple hard-coded manifest.
Here's what I would with more time for an application meant to be in production:
- Package the application as a Flask API to remove the `sleep infinite` and expose it with a `Service` and `Ingress` to query it externally.
- Add a `HorizontalPodAutoscaler` to scale up if need be.
- Package the Kubernetes manifests as a Helm chart and variabilize what may change (name, resources, extra envs, etc.)

## Part 3 - CI/CD

The CI pipeline is built with GitHub actions (see `.github/workflows`) with the following steps:

- `test`: run available Python tests
  - (improvement) Add code coverage
- `audit`: run `pip audit` on the `requirements.txt` to identify vulnerabilities
  - (improvement) Split `requirements.txt` into production and dev requirements to limit attack surface.
- `build-and-push-image`: build and publish the Docker image on GitHub Container Registry and validate it using Trivy.

### TODO

The CD part is not actually implemented. Here's what I would do with more time + a public Kubernetes cluster:
- Either add a GitHub action to apply the manifests with `kubectl` or install the chart with `helm` after authenticating to the Kubernetes control plane
- Or declare an ArgoCD application for the Helm chart if ArgoCD is installed in the cluster, and use the `argocd` CLI to update the tag used by the application.

The easier way to deploy would be to use a PaaS (for instance fly.io).

## Part 4

Here are solutions that could extract the root DNS from the provided files.

Simple solution using `sed` to remove protocols and potential trailing dot, `tr` to switch to lower case and `cut` to only keep the last two parts:

```
$ cat input.txt | sed -e "s/http:\/\///" -e "s/https:\/\///" -e "s/\.$//" | tr '[:upper:]' '[:lower:]' | rev | cut -d'.' -f 1-2 | rev | sort | uniq
amazon.com
facebook.com
google.com
tiktok.com
```

Assuming we only have `.com` domains, we can use a simple Regex with `grep`:

```
$ cat input.txt | grep -o '[a-zA-Z]*.com' | tr '[:upper:]' '[:lower:]' | sort | uniq
amazon.com
facebook.com
google.com
tiktok.com
```

Using `perl` to be able to capture Regex groups, we can use a more generic expression that would match other TLD and manage the potential trailing dot:

```
$ cat input.txt | perl -lne 'print $1 while /([a-zA-Z]*\.[a-z]*)(\.?)$/g' | tr '[:upper:]' '[:lower:]' | sort | uniq
amazon.com
facebook.com
google.com
tiktok.com
```

## Bonus - CS concepts

The script developed for the case study could be used to build a directed graph for a website:
- Start at the root `/` which is our first node.
- List all links (= edges) from it to build our next nodes.
- The graph is directed since we go from a page TO another one.
- For each new node, repeat if the node has not already been visited.

After that, we'll have a directed graph to navigate the website, and we're _this_ close to make an [Advent of Code](https://adventofcode.com/)
problem where we need to painfully reimplement Djikstra's shortest path algorithm while it's snowing outside. 🎅

If we modified our script to also explore external websites instead of limiting ourselves to a single host,
we could also measure websites popularity with the same approach as Google's original [PageRank algorithm](https://en.wikipedia.org/wiki/PageRank).

To do that, we would need to build the same kind of directed graph as before, but this time on multiple hosts.
After that, we would have to count the number of links to a page to determine its popularity: the higher the count
of links, the more popular the website.

Of course, this (rather) naive approach would likely not generate quality insights given the structure of websites that
try to game the system with lots of links directing to spam pages. Other algorithms would probably be more interesting
to discover and try out!