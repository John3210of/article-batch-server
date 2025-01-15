'''

data = [
    {
        "title": "Kubernetes Basics",
        "contents": "An introduction to Kubernetes and container orchestration.",
        "link": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
        "categoryTitle": "kubernetes"
    },
    {
        "title": "Kubernetes Best Practices",
        "contents": "Learn the best practices for running Kubernetes in production.",
        "link": "https://kubernetes.io/docs/setup/best-practices/",
        "categoryTitle": "kubernetes"
    },
    {
        "title": "Kubernetes Security",
        "contents": "Guide to securing your Kubernetes cluster.",
        "link": "https://kubernetes.io/docs/concepts/security/",
        "categoryTitle": "kubernetes"
    },
    {
        "title": "Kubernetes Advanced Topics",
        "contents": "Explore advanced Kubernetes topics and use cases.",
        "link": "https://kubernetes.io/docs/tutorials/advanced/",
        "categoryTitle": "kubernetes"
    },
    {
        "title": "Getting Started with Helm",
        "contents": "A guide to getting started with Helm package manager.",
        "link": "https://helm.sh/docs/intro/quickstart/",
        "categoryTitle": "helm"
    },
    {
        "title": "Helm Chart Repositories",
        "contents": "How to manage Helm chart repositories effectively.",
        "link": "https://helm.sh/docs/topics/chart_repository/",
        "categoryTitle": "helm"
    },
    {
        "title": "Creating Helm Charts",
        "contents": "Learn how to create custom Helm charts for your applications.",
        "link": "https://helm.sh/docs/topics/charts/",
        "categoryTitle": "helm"
    },
    {
        "title": "Helm Advanced Configuration",
        "contents": "Understand advanced Helm configuration options.",
        "link": "https://helm.sh/docs/helm/",
        "categoryTitle": "helm"
    },
    {
        "title": "Docker Basics",
        "contents": "Introduction to Docker and containerization.",
        "link": "https://www.docker.com/resources/what-container/",
        "categoryTitle": "docker"
    },
    {
        "title": "Docker Compose Guide",
        "contents": "Learn how to define and run multi-container Docker applications.",
        "link": "https://docs.docker.com/compose/",
        "categoryTitle": "docker"
    },
    {
        "title": "Docker Security",
        "contents": "Best practices for securing Docker containers.",
        "link": "https://docs.docker.com/engine/security/",
        "categoryTitle": "docker"
    },
    {
        "title": "Docker Networking",
        "contents": "Understand Docker networking concepts and configurations.",
        "link": "https://docs.docker.com/network/",
        "categoryTitle": "docker"
    },
    {
        "title": "Python Introduction",
        "contents": "Getting started with Python programming.",
        "link": "https://www.python.org/about/gettingstarted/",
        "categoryTitle": "python"
    },
    {
        "title": "Python Libraries Guide",
        "contents": "Comprehensive guide to Python's standard libraries.",
        "link": "https://docs.python.org/3/library/",
        "categoryTitle": "python"
    },
    {
        "title": "Python Data Analysis",
        "contents": "How to perform data analysis using Python.",
        "link": "https://pandas.pydata.org/docs/",
        "categoryTitle": "python"
    },
    {
        "title": "Python Advanced Programming",
        "contents": "Advanced Python programming techniques.",
        "link": "https://realpython.com/",
        "categoryTitle": "python"
    },
    {
        "title": "Java Basics",
        "contents": "Introduction to Java programming language.",
        "link": "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/",
        "categoryTitle": "java"
    },
    {
        "title": "Java Concurrency",
        "contents": "Learn about concurrency and multi-threading in Java.",
        "link": "https://docs.oracle.com/javase/tutorial/essential/concurrency/",
        "categoryTitle": "java"
    },
    {
        "title": "Java Streams",
        "contents": "Guide to Java Streams and functional programming.",
        "link": "https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html",
        "categoryTitle": "java"
    },
    {
        "title": "Java Spring Framework",
        "contents": "Introduction to Java's Spring Framework.",
        "link": "https://spring.io/guides",
        "categoryTitle": "java"
    },
    {
        "title": "JavaScript Basics",
        "contents": "Getting started with JavaScript programming.",
        "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics",
        "categoryTitle": "javascript"
    },
    {
        "title": "JavaScript ES6 Features",
        "contents": "Learn the latest ES6 features in JavaScript.",
        "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference",
        "categoryTitle": "javascript"
    },
    {
        "title": "JavaScript Debugging",
        "contents": "How to debug JavaScript code effectively.",
        "link": "https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Debugging/Debugging_JavaScript",
        "categoryTitle": "javascript"
    },
    {
        "title": "JavaScript DOM Manipulation",
        "contents": "Learn to manipulate the DOM with JavaScript.",
        "link": "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model",
        "categoryTitle": "javascript"
    }
]
for d in data:
    response = ArticleService.create_articles(d)

'''