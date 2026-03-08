from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

# Load environment variables

app = Flask(__name__)
app.secret_key = "1234"


# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Course Details Database - All 12 Internship Tracks
COURSES_DB = {
    'genai-ml': {
        'title': 'GenAI / ML - Mastery Program',
        'description': 'Master Generative AI and Machine Learning from fundamentals to advanced applications including LLMs, neural networks, and real-world deployment.',
        'level': 'Beginner to Advanced',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Weekly Projects',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Basic computer knowledge', 'No prior ML experience required', 'Willingness to practice regularly', 'Dedication to learning AI fundamentals'],
        'learnings': ['Python basics for ML', 'Neural networks and deep learning', 'Large Language Models (LLMs)', 'Prompt engineering', 'Model training and deployment', 'Real-world AI projects'],
        'about': 'GenXEraAI is committed to providing practical AI and ML training to help students become industry-ready. We focus on hands-on projects and real-world applications. Our comprehensive curriculum covers everything from ML basics to advanced LLM fine-tuning, ensuring you\'re equipped with the latest skills needed in the AI industry.',
        'stats': {'enrolled': '500+', 'completion': '87%', 'rating': '4.7/5'},
        'experts': [
            {'expertise': 'ML & AI Architecture', 'description': 'Former Senior ML Engineer at leading AI company with 12+ years experience', 'icon': 'bi bi-cpu'},
            {'expertise': 'Deep Learning Specialist', 'description': 'Published researcher in neural networks with expertise in computer vision', 'icon': 'bi bi-diagram-3'},
            {'expertise': 'LLM Expert', 'description': 'Specializes in transformer models and fine-tuning with real-world deployments', 'icon': 'fa-solid fa-brain'},
            {'expertise': 'Data Engineering', 'description': 'Expert in data pipelines and scalable ML infrastructure', 'icon': 'bi bi-database'}
        ],
        'venue': {'location': 'GenXEraAI Center, Tech Hub 172-A & 172-B, Innovation District', 'schedule': ['Monday - Friday: 5:00 PM - 7:00 PM', 'Saturday: 5:00 PM - 7:00 PM (Optional)', 'Online sessions available']},
        'syllabus': [
            {'week': 'Week 1: Python, ML Basics & Fundamentals', 'hours': '24 hours', 'topics': ['NumPy, Pandas, Matplotlib', 'Data preprocessing techniques', 'Supervised vs Unsupervised learning', 'Linear & Logistic Regression', 'Decision Trees & Random Forests']},
            {'week': 'Week 2: Neural Networks & Deep Learning', 'hours': '24 hours', 'topics': ['Perceptrons & Backpropagation', 'TensorFlow & Keras', 'CNN for image classification', 'RNN & LSTM for sequences', 'Transfer learning']},
            {'week': 'Week 3: Generative AI & LLMs', 'hours': '24 hours', 'topics': ['Transformer architecture', 'Attention mechanisms', 'Prompt engineering', 'Fine-tuning LLMs']},
            {'week': 'Week 4: Deployment & Capstone', 'hours': '24 hours', 'topics': ['Model deployment strategies', 'Docker & containerization', 'Real-world capstone project', 'Portfolio building']}
        ]
    },
    'data-science': {
        'title': 'Data Science + Data Engineering Program',
        'description': 'Learn data analysis, SQL, ETL pipelines, and analytics visualization for real-world data challenges.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Weekly Projects',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Basic SQL knowledge', 'Python fundamentals', 'Statistics basics'],
        'learnings': ['Advanced SQL', 'ETL pipeline design', 'Data visualization', 'Big Data tools', 'Analytics projects', 'Data warehousing'],
        'about': 'Master the art of extracting insights from data. Learn to build scalable ETL pipelines, create compelling visualizations, and make data-driven decisions. Work with real-world datasets and enterprise tools.',
        'stats': {'enrolled': '300+', 'completion': '84%', 'rating': '4.6/5'},
        'experts': [
            {'expertise': 'Data Engineering Lead', 'description': '10+ years in building scalable data systems and pipelines', 'icon': 'bi bi-diagram-2'},
            {'expertise': 'Analytics Expert', 'description': 'Specialized in business intelligence and advanced BI tools', 'icon': 'bi bi-graph-up'}
        ],
        'venue': {'location': 'Tech Hub Center, Analytics Division', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Saturday: 3:00 PM - 5:00 PM']},
        'syllabus': [
            {'week': 'Week 1: SQL, Python & Data Processing', 'hours': '24 hours', 'topics': ['Complex queries & joins', 'Window functions', 'Pandas & NumPy mastery', 'Data cleaning & transformation', 'Feature engineering']},
            {'week': 'Week 2: ETL Pipelines & Warehousing', 'hours': '24 hours', 'topics': ['Pipeline design patterns', 'Data warehousing basics', 'Apache Spark introduction']},
            {'week': 'Week 3: Data Visualization & BI', 'hours': '24 hours', 'topics': ['Tableau and Power BI', 'Interactive dashboards', 'Business intelligence']},
            {'week': 'Week 4: End-to-End Capstone', 'hours': '24 hours', 'topics': ['End-to-end data project', 'Performance optimization', 'Presentation skills']}
        ]
    },
    'cybersecurity': {
        'title': 'Cybersecurity Fundamentals Program',
        'description': 'Learn network security, ethical hacking, and vulnerability assessment to protect organizations from cyber threats.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Hands-on Labs',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Basic networking knowledge', 'Understanding of operating systems', 'Command line familiarity'],
        'learnings': ['Network security basics', 'Ethical hacking techniques', 'Vulnerability assessment', 'Penetration testing', 'Security compliance', 'Incident response'],
        'about': 'Become a certified cybersecurity professional. Learn to identify vulnerabilities, conduct penetration tests, and defend against modern threats. Hands-on labs with real-world scenarios.',
        'stats': {'enrolled': '250+', 'completion': '82%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'Security Architect', 'description': 'Former CISO with expertise in enterprise security', 'icon': 'bi bi-shield-lock'},
            {'expertise': 'Penetration Tester', 'description': 'Certified ethical hacker with 8+ years of experience', 'icon': 'bi bi-shield-check'}
        ],
        'venue': {'location': 'Security Lab, Tech Hub Center', 'schedule': ['Monday - Friday: 7:00 PM - 9:00 PM', 'Lab access: 24/7']},
        'syllabus': [
            {'week': 'Week 1: Networks & Web Security', 'hours': '24 hours', 'topics': ['OSI model & TCP/IP', 'Network scanning', 'OWASP Top 10', 'SQL injection', 'XSS & CSRF']},
            {'week': 'Week 2: Penetration Testing', 'hours': '24 hours', 'topics': ['Reconnaissance', 'Vulnerability scanning', 'Exploitation techniques']},
            {'week': 'Week 3: Cryptography & Compliance', 'hours': '24 hours', 'topics': ['Encryption basics', 'SSL/TLS', 'GDPR and compliance']},
            {'week': 'Week 4: Capstone Security Lab', 'hours': '24 hours', 'topics': ['Full penetration test', 'Report writing', 'Security recommendations']}
        ]
    },
    'cloud-aws': {
        'title': 'Cloud Computing (AWS/Azure) Program',
        'description': 'Master cloud platforms AWS and Azure. Learn to deploy, manage, and scale applications in the cloud.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Basic server knowledge', 'Understanding of networking', 'Familiarity with Linux/Windows'],
        'learnings': ['AWS EC2, S3, Lambda', 'Azure VMs and App Services', 'Database management', 'Serverless architecture', 'Cloud security', 'Cost optimization'],
        'about': 'Transform your career with cloud expertise. Deploy real applications on AWS and Azure, manage databases, implement security, and optimize costs. Industry-standard certifications covered.',
        'stats': {'enrolled': '400+', 'completion': '85%', 'rating': '4.7/5'},
        'experts': [
            {'expertise': 'AWS Solutions Architect', 'description': 'AWS certified with enterprise deployment experience', 'icon': 'bi bi-cloud'},
            {'expertise': 'Azure Cloud Expert', 'description': 'Microsoft certified cloud professional', 'icon': 'bi bi-cloud-fill'}
        ],
        'venue': {'location': 'Cloud Lab, Innovation Center', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Sandbox access: 24/7']},
        'syllabus': [
            {'week': 'Week 1: Fundamentals & AWS Core', 'hours': '24 hours', 'topics': ['Cloud concepts & Cost models', 'AWS EC2, S3, RDS', 'IAM & Security']},
            {'week': 'Week 2: Azure Services', 'hours': '24 hours', 'topics': ['Virtual machines', 'App Service', 'Cosmos DB']},
            {'week': 'Week 3: Serverless & Containers', 'hours': '24 hours', 'topics': ['Lambda/Functions', 'Docker basics', 'Kubernetes intro']},
            {'week': 'Week 4: Deployment & Scaling', 'hours': '24 hours', 'topics': ['Multi-tier applications', 'Auto-scaling', 'Disaster recovery', 'Real-world project']}
        ]
    },
    'devops': {
        'title': 'DevOps Engineering Program',
        'description': 'Master CI/CD pipelines, infrastructure automation, and containerization with Docker and Kubernetes.',
        'level': 'Advanced',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Hands-on Labs',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Linux command line proficiency', 'Basic programming', 'Git fundamentals'],
        'learnings': ['CI/CD pipelines', 'Infrastructure as Code', 'Docker and containers', 'Kubernetes orchestration', 'Monitoring and logging', 'DevOps best practices'],
        'about': 'Become a DevOps engineer and bridge the gap between development and operations. Learn to automate deployments, manage infrastructure, and build resilient systems.',
        'stats': {'enrolled': '280+', 'completion': '86%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'DevOps Lead', 'description': 'Led DevOps transformation at Fortune 500 company', 'icon': 'bi bi-gear-wide-connected'},
            {'expertise': 'Kubernetes Expert', 'description': 'Certified Kubernetes application developer', 'icon': 'bi bi-diagram-3'}
        ],
        'venue': {'location': 'DevOps Lab, Tech Hub', 'schedule': ['Monday - Friday: 7:00 PM - 9:00 PM', 'Lab servers: 24/7 access']},
        'syllabus': [
            {'week': 'Week 1: CI/CD & Automation', 'hours': '24 hours', 'topics': ['Jenkins setup', 'GitLab CI', 'Pipeline design']},
            {'week': 'Week 2: Infrastructure as Code & Docker', 'hours': '24 hours', 'topics': ['Terraform & Ansible', 'Containerization', 'Docker compose']},
            {'week': 'Week 3: Kubernetes', 'hours': '24 hours', 'topics': ['K8s architecture', 'Deployments and services', 'Helm charts']},
            {'week': 'Week 4: Monitoring & Tuning', 'hours': '24 hours', 'topics': ['Prometheus and Grafana', 'ELK stack', 'Performance optimization', 'Final Project']}
        ]
    },
    'salesforce-dev': {
        'title': 'Salesforce Development Program',
        'description': 'Master Salesforce platform development with Apex, Lightning Web Components, and CRM customization for enterprise solutions.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Basic programming knowledge', 'Understanding of databases', 'CRM concepts'],
        'learnings': ['Salesforce fundamentals', 'Apex programming', 'Lightning Web Components', 'SOQL and SOSL', 'Integration patterns', 'Salesforce certifications'],
        'about': 'Become a certified Salesforce developer and build powerful CRM solutions. Learn to customize Salesforce, develop Lightning components, and integrate with external systems. Prepare for Salesforce certifications.',
        'stats': {'enrolled': '340+', 'completion': '85%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'Salesforce Architect', 'description': 'Certified Technical Architect with 10+ years enterprise experience', 'icon': 'bi bi-cloud-check'},
            {'expertise': 'Lightning Developer', 'description': 'Expert in Lightning Web Components and Aura framework', 'icon': 'bi bi-lightning-charge'}
        ],
        'venue': {'location': 'Salesforce Lab, CRM Center', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Trailhead support: 24/7']},
        'syllabus': [
            {'week': 'Week 1: Salesforce Fundamentals', 'hours': '24 hours', 'topics': ['Platform overview', 'Data model & objects', 'Security & sharing']},
            {'week': 'Week 2: Apex & Customization', 'hours': '24 hours', 'topics': ['Apex syntax', 'Triggers & classes', 'Governor limits', 'Test classes']},
            {'week': 'Week 3: LWC & UI', 'hours': '24 hours', 'topics': ['LWC fundamentals', 'Component lifecycle', 'Event handling', 'Data binding']},
            {'week': 'Week 4: Integration & Projects', 'hours': '24 hours', 'topics': ['SOQL/SOSL', 'APIs & Webhooks', 'End-to-end CRM solution']}
        ]
    },
    'full-stack-web': {
        'title': 'Full-Stack Web Development Program',
        'description': 'Build complete web applications from front-end to back-end using React, Node.js, and databases.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['HTML/CSS basics', 'JavaScript fundamentals', 'Problem-solving skills'],
        'learnings': ['React and Vue.js', 'Node.js and Express', 'REST APIs and GraphQL', 'Database design', 'Authentication and authorization', 'Deployment and DevOps'],
        'about': 'Become a full-stack developer and build production-ready web applications. Master modern frameworks, databases, and deployment strategies.',
        'stats': {'enrolled': '600+', 'completion': '88%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'Frontend Architect', 'description': 'Expert in React and modern JavaScript frameworks', 'icon': 'bi bi-window-desktop'},
            {'expertise': 'Backend Engineer', 'description': 'Specialist in Node.js, API design, and databases', 'icon': 'bi bi-code-slash'}
        ],
        'venue': {'location': 'Web Development Center', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Project mentoring: Weekends']},
        'syllabus': [
            {'week': 'Week 1: Fundamentals & React Basics', 'hours': '24 hours', 'topics': ['HTML5, CSS3, JS ES6+', 'React Components & JSX', 'State, props, Hooks']},
            {'week': 'Week 2: Advanced React, Node & Express', 'hours': '24 hours', 'topics': ['Context API & Redux', 'Node.js server setup', 'Routing & Middleware']},
            {'week': 'Week 3: Databases & APIs', 'hours': '24 hours', 'topics': ['SQL & NoSQL', 'REST API design', 'GraphQL basics']},
            {'week': 'Week 4: Deployment & Full Stack Projects', 'hours': '24 hours', 'topics': ['Heroku/Docker deployment', 'Full-stack integration', 'Capstone Project']}
        ]
    },
    'mobile-apps': {
        'title': 'Mobile App Development Program',
        'description': 'Build native and cross-platform mobile apps for iOS and Android using Flutter and React Native.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Object-oriented programming', 'Basic UI/UX understanding', 'Mobile fundamentals'],
        'learnings': ['Flutter framework', 'React Native basics', 'State management', 'APIs integration', 'App store deployment', 'Performance optimization'],
        'about': 'Learn to develop beautiful, performant mobile applications. Master cross-platform development with Flutter and publish apps to App Store and Google Play.',
        'stats': {'enrolled': '350+', 'completion': '81%', 'rating': '4.6/5'},
        'experts': [
            {'expertise': 'Flutter Developer', 'description': 'Expert in cross-platform mobile development', 'icon': 'bi bi-phone-fill'},
            {'expertise': 'Mobile UX/UI', 'description': 'Specialist in mobile app design and user experience', 'icon': 'bi bi-app-indicator'}
        ],
        'venue': {'location': 'Mobile Lab, Tech Center', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Device lab: 24/7 access']},
        'syllabus': [
            {'week': 'Week 1: Dart & Flutter UI', 'hours': '24 hours', 'topics': ['Dart programming', 'Flutter widgets', 'Material Design & Layouts']},
            {'week': 'Week 2: Advanced UI & State', 'hours': '24 hours', 'topics': ['Responsive design', 'Custom widgets', 'State Management (Provider/GetX)']},
            {'week': 'Week 3: Networking & Backend', 'hours': '24 hours', 'topics': ['REST API integration', 'JSON parsing', 'Authentication']},
            {'week': 'Week 4: Deployment & Publishing', 'hours': '24 hours', 'topics': ['App store optimization', 'Google Play release', 'Capstone App']}
        ]
    },
    'blockchain': {
        'title': 'Blockchain & Web3 Development Program',
        'description': 'Master blockchain technology, smart contracts, and Web3 development with Solidity and Ethereum.',
        'level': 'Advanced',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Solid programming background', 'Cryptography basics', 'Understanding of distributed systems'],
        'learnings': ['Blockchain fundamentals', 'Solidity smart contracts', 'Ethereum development', 'Web3.js and Ethers.js', 'DeFi protocols', 'NFT development'],
        'about': 'Enter the Web3 revolution. Learn to build decentralized applications, write secure smart contracts, and understand blockchain architecture.',
        'stats': {'enrolled': '180+', 'completion': '79%', 'rating': '4.7/5'},
        'experts': [
            {'expertise': 'Blockchain Architect', 'description': 'Expert in blockchain design and smart contract security', 'icon': 'bi bi-currency-bitcoin'},
            {'expertise': 'Web3 Developer', 'description': 'Specializes in DeFi and NFT protocols', 'icon': 'bi bi-link-45deg'}
        ],
        'venue': {'location': 'Web3 Lab, Innovation Hub', 'schedule': ['Monday - Friday: 7:00 PM - 9:00 PM', 'Testnet: 24/7 access']},
        'syllabus': [
            {'week': 'Week 1: Blockchain Fundamentals', 'hours': '24 hours', 'topics': ['Bitcoin & Ethereum basics', 'Consensus mechanisms', 'Cryptography']},
            {'week': 'Week 2: Smart Contracts & Web3', 'hours': '24 hours', 'topics': ['Solidity syntax', 'Contract design', 'Web3.js interaction']},
            {'week': 'Week 3: DeFi & NFTs', 'hours': '24 hours', 'topics': ['ERC-20 tokens', 'NFT standards', 'Lending protocols']},
            {'week': 'Week 4: Security & Mainnet', 'hours': '24 hours', 'topics': ['Contract auditing', 'Security best practices', 'Final Deployment']}
        ]
    },
    'iot': {
        'title': 'IoT & Embedded Systems Program',
        'description': 'Design and develop Internet of Things applications using Arduino, Raspberry Pi, and sensor integration.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Hands-on Labs',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Electronics basics', 'Programming fundamentals', 'Circuit understanding'],
        'learnings': ['Arduino programming', 'Sensor integration', 'Cloud connectivity', 'Protocol: MQTT, HTTP', 'Real-time data processing', 'IoT security'],
        'about': 'Build connected smart devices and IoT systems. Learn to interface with sensors, create IoT networks, and develop real-world applications.',
        'stats': {'enrolled': '200+', 'completion': '82%', 'rating': '4.7/5'},
        'experts': [
            {'expertise': 'IoT Architect', 'description': 'Expert in IoT system design and scalability', 'icon': 'bi bi-cpu-fill'},
            {'expertise': 'Embedded Systems', 'description': 'Specialist in firmware and hardware integration', 'icon': 'bi bi-router-fill'}
        ],
        'venue': {'location': 'IoT Lab, Maker Space', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Open lab: Weekends']},
        'syllabus': [
            {'week': 'Week 1: Hardware & Sensors', 'hours': '24 hours', 'topics': ['Arduino & Microcontrollers', 'Circuit basics', 'Sensor types & Data acquisition']},
            {'week': 'Week 2: Communication & Protocols', 'hours': '24 hours', 'topics': ['I2C, SPI, Serial', 'Wireless basics', 'Motor control']},
            {'week': 'Week 3: Cloud IoT', 'hours': '24 hours', 'topics': ['MQTT protocol', 'AWS IoT', 'Data visualization']},
            {'week': 'Week 4: Smart Systems Project', 'hours': '24 hours', 'topics': ['Smart home integration', 'Environmental monitoring', 'Capstone System']}
        ]
    },
    'ui-ux': {
        'title': 'UI/UX Design Program',
        'description': 'Master user interface and user experience design. Learn Figma, wireframing, prototyping, and design systems.',
        'level': 'Beginner to Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Design fundamentals', 'Basic visual design', 'Understanding of UX principles'],
        'learnings': ['Figma mastery', 'User research methods', 'Wireframing & prototyping', 'Design systems', 'Interaction design', 'Usability testing'],
        'about': 'Create beautiful, user-centric designs. Learn the complete design process from research to prototyping, and deliver exceptional user experiences.',
        'stats': {'enrolled': '280+', 'completion': '87%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'UX/UI Designer', 'description': 'Led design teams at tech startups and companies', 'icon': 'bi bi-palette-fill'},
            {'expertise': 'Design Systems Expert', 'description': 'Specialist in scalable design systems', 'icon': 'bi bi-brush-fill'}
        ],
        'venue': {'location': 'Design Studio, Creative Hub', 'schedule': ['Monday - Friday: 5:00 PM - 7:00 PM', 'Design critiques: Saturdays']},
        'syllabus': [
            {'week': 'Week 1: Design Principles', 'hours': '24 hours', 'topics': ['Color theory', 'Typography', 'Layout principles']},
            {'week': 'Week 2: User Research', 'hours': '24 hours', 'topics': ['User interviews', 'Personas', 'User journeys']},
            {'week': 'Week 3: Figma & Prototyping', 'hours': '24 hours', 'topics': ['Figma workspace', 'Components', 'Interactive prototypes']},
            {'week': 'Week 4: Design Systems & Testing', 'hours': '24 hours', 'topics': ['Design tokens', 'Usability testing', 'Handoff to developers']}
        ]
    },
    'embedded-systems': {
        'title': 'Embedded Systems Program',
        'description': 'Master embedded systems design and development. Learn to interface with hardware, write firmware, and build real-time applications.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['C/C++ basics', 'Electronics fundamentals', 'Problem-solving skills'],
        'learnings': ['Microcontroller architecture', 'Firmware development', 'Hardware interfacing', 'Real-time operating systems', 'Protocol: UART, I2C, SPI', 'Embedded C programming'],
        'about': 'Enter the world of embedded systems. Learn to design and program systems that power everything from household appliances to industrial automation. Hands-on projects with microcontrollers and sensors.',
        'stats': {'enrolled': '250+', 'completion': '80%', 'rating': '4.7/5'},
        'experts': [
            {'expertise': 'Embedded Architect', 'description': 'Specialist in hardware-software integration, 10+ years experience', 'icon': 'bi bi-cpu'},
            {'expertise': 'Firmware Engineer', 'description': 'Expert in low-level drivers and RTOS with industry experience', 'icon': 'fa-solid fa-microchip'}
        ],
        'venue': {'location': 'Embedded Systems Lab, Tech Center', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Lab access: 24/7']},
        'syllabus': [
            {'week': 'Week 1: Embedded C & Architecture', 'hours': '24 hours', 'topics': ['C for embedded systems', 'Microcontroller architecture', 'Registers and GPIOs', 'Timer and interrupts']},
            {'week': 'Week 2: Interfacing & Protocols', 'hours': '24 hours', 'topics': ['ADC & DAC', 'UART communication', 'I2C & SPI protocols', 'Sensor interfacing']},
            {'week': 'Week 3: RTOS & Advanced Topics', 'hours': '24 hours', 'topics': ['RTOS fundamentals', 'Task scheduling', 'Memory management', 'Power optimization']},
            {'week': 'Week 4: Project & Deployment', 'hours': '24 hours', 'topics': ['System design patterns', 'Debugging techniques', 'Complete embedded project']}
        ]
    },
    'vlsi': {
        'title': 'VLSI Design & Verification Program',
        'description': 'Master Very Large Scale Integration (VLSI) chip design, Verilog HDL, and functional verification.',
        'level': 'Advanced',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Hands-on Labs',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Digital Electronics', 'Basic programming knowledge', 'Circuit theory'],
        'learnings': ['Digital design fundamentals', 'Verilog HDL programming', 'FPGA implementation', 'Functional verification', 'CMOS design', 'STA basics'],
        'about': 'Dive into the core of hardware engineering. Learn to design, simulate, and verify complex digital circuits and systems for modern semiconductor technologies.',
        'stats': {'enrolled': '120+', 'completion': '82%', 'rating': '4.7/5'},
        'experts': [
            {'expertise': 'VLSI Architect', 'description': 'Senior hardware designer with tape-out experience', 'icon': 'fa-solid fa-microchip'},
            {'expertise': 'Verification Engineer', 'description': 'Expert in UVM and functional verification', 'icon': 'bi bi-cpu-fill'}
        ],
        'venue': {'location': 'Hardware Lab, Tech Center', 'schedule': ['Monday - Friday: 5:00 PM - 7:00 PM', 'Simulator access: 24/7']},
        'syllabus': [
            {'week': 'Week 1: Digital Design Review', 'hours': '24 hours', 'topics': ['Combinational logic', 'Sequential circuits', 'Finite State Machines']},
            {'week': 'Week 2: Verilog HDL', 'hours': '24 hours', 'topics': ['Verilog syntax', 'Behavioral modeling', 'Testbenches', 'Simulation']},
            {'week': 'Week 3: Advanced Verification', 'hours': '24 hours', 'topics': ['SystemVerilog basics', 'Assertions', 'Coverage-driven verification']},
            {'week': 'Week 4: FPGA & Project', 'hours': '24 hours', 'topics': ['FPGA synthesis', 'Timing analysis', 'Capstone project implementation']}
        ]
    },
    'game-dev': {
        'title': 'Game Development Program',
        'description': 'Create immersive 2D and 3D games using industry-standard game engines like Unity and Unreal.',
        'level': 'Intermediate',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['C# or C++ basics', 'Passion for gaming', 'Basic math/physics'],
        'learnings': ['Unity/Unreal basics', 'Game physics and mechanics', '3D math for games', 'UI/UX for gaming', 'Enemy AI programming', 'Multiplayer basics'],
        'about': 'Turn your gaming passion into a profession. Build interactive and visually stunning games from scratch while understanding core game design principles.',
        'stats': {'enrolled': '150+', 'completion': '88%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'Game Producer', 'description': 'Published creator of top-charting indie games', 'icon': 'bi bi-controller'},
            {'expertise': 'Technical Artist', 'description': 'Specialist in shaders, rigging, and optimization', 'icon': 'bi bi-brush-fill'}
        ],
        'venue': {'location': 'Game Station, Media Lab', 'schedule': ['Monday - Friday: 6:00 PM - 8:00 PM', 'Engine access: 24/7']},
        'syllabus': [
            {'week': 'Week 1: Engine Fundamentals', 'hours': '24 hours', 'topics': ['Scene setup', 'Game objects', 'Basic scripts', 'Asset management']},
            {'week': 'Week 2: Core Mechanics', 'hours': '24 hours', 'topics': ['Player movement', 'Collisions and Physics', 'Camera controls', 'Input systems']},
            {'week': 'Week 3: Visuals & UI', 'hours': '24 hours', 'topics': ['Lighting and materials', 'Particle systems', 'Game UI design', 'Audio implementation']},
            {'week': 'Week 4: AI & Publishing', 'hours': '24 hours', 'topics': ['Enemy state machines', 'Level design finish', 'Game polish', 'Exporting and publishing']}
        ]
    },
    'offline-internship': {
        'title': 'Offline Industrial Program (Final Year Students)',
        'description': 'Exclusive 3-month comprehensive offline internship program designed for final year students. Includes certification and one major real-time project.',
        'level': 'Advanced',
        'duration': '3 Months',
        'hours': '120 Hours',
        'format': 'Offline Project-Based',
        'total_weeks': '12 Weeks',
        'price': '3999',
        'original_price': '5999',
        'prerequisites': ['Final year standing', 'Core programming fundamentals', 'Commitment to offline sessions'],
        'learnings': ['Real-time project development', 'Industry standard coding practices', 'Team collaboration', 'Software deployment', 'Technical documentation', 'Interview preparation'],
        'about': 'An intensive 3-month offline internship program that bridges the gap between academic learning and industry requirements. Perfect for final year students needing a major real-time project.',
        'stats': {'enrolled': '50+', 'completion': '95%', 'rating': '4.9/5'},
        'experts': [
            {'expertise': 'Project Director', 'description': 'Industry veteran with 15+ years experience in managing enterprise projects', 'icon': 'bi bi-person-workspace'},
            {'expertise': 'Technical Lead', 'description': 'Expert in modern tech stacks and system architecture', 'icon': 'bi bi-diagram-3-fill'}
        ],
        'venue': {'location': 'Main Campus / Tech Center', 'schedule': ['Monday - Friday: 10:00 AM - 5:00 PM', 'Offline attendance mandatory']},
        'syllabus': [
            {'week': 'Month 1: Foundation & Planning', 'hours': '40 hours', 'topics': ['Project scope definition', 'Requirements gathering', 'Tech stack selection', 'System design']},
            {'week': 'Month 2: Core Development', 'hours': '40 hours', 'topics': ['Backend architecture', 'Frontend integration', 'Database modeling', 'API development']},
            {'week': 'Month 3: Testing & Delivery', 'hours': '40 hours', 'topics': ['Quality assurance', 'Performance testing', 'Project documentation', 'Final presentation']}
        ]
    },
    'cloud-devops': {
        'title': 'Cloud Computing & DevOps Program',
        'description': 'Master AWS, Docker, Kubernetes, and CI/CD pipelines to deploy scalable applications.',
        'level': 'Advanced',
        'duration': '4 Weeks',
        'hours': '24 Hours',
        'format': 'Project-Based',
        'total_weeks': '4 Weeks',
        'prerequisites': ['Linux basics', 'Understanding of networking', 'Basic programming'],
        'learnings': ['AWS Infrastructure', 'Docker containerization', 'Kubernetes orchestration', 'Jenkins CI/CD', 'Terraform (IaC)', 'Serverless concepts'],
        'about': 'Bridge the gap between development and operations. Learn to automate infrastructure, containerize applications, and build robust deployment pipelines.',
        'stats': {'enrolled': '210+', 'completion': '84%', 'rating': '4.8/5'},
        'experts': [
            {'expertise': 'Cloud Architect', 'description': 'AWS Certified Solutions Architect Professional', 'icon': 'bi bi-cloud-arrow-up'},
            {'expertise': 'DevOps Engineer', 'description': 'Expert in container orchestration and automation', 'icon': 'bi bi-gear-wide-connected'}
        ],
        'venue': {'location': 'Cloud Lab, Tech Center', 'schedule': ['Monday - Friday: 7:00 PM - 9:00 PM', 'Cloud credits provided']},
        'syllabus': [
            {'week': 'Week 1: Linux & Docker', 'hours': '24 hours', 'topics': ['Linux administration', 'Shell scripting', 'Docker basics', 'Containerizing apps']},
            {'week': 'Week 2: AWS Essentials', 'hours': '24 hours', 'topics': ['EC2 & VPCs', 'S3 & Databases', 'IAM and Security', 'Cloud computing paradigms']},
            {'week': 'Week 3: CI/CD Pipelines', 'hours': '24 hours', 'topics': ['Git workflows', 'Jenkins automation', 'GitHub Actions', 'Automated testing']},
            {'week': 'Week 4: K8s & IaC', 'hours': '24 hours', 'topics': ['Kubernetes architecture', 'Deployments & Services', 'Terraform basics', 'Final deployment project']}
        ]
    }
}

@app.route('/course/<course>', methods=['GET'])
def course_details(course):
    course_data = COURSES_DB.get(course)
    if not course_data:
        return redirect(url_for('index'))
    return render_template('course-details.html', course_data=course_data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'admin':
        session['user'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid credentials/username')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found - The requested feature or route has been removed.", 404

if __name__ == '__main__':
    app.run(debug=True)
