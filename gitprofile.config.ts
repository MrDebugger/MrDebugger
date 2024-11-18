// gitprofile.config.ts

const CONFIG = {
  github: {
    username: 'MrDebugger', // Your GitHub org/user name. (This is the only required config)
  },
  /**
   * If you are deploying to https://<USERNAME>.github.io/, for example your repository is at https://github.com/arifszn/arifszn.github.io, set base to '/'.
   * If you are deploying to https://<USERNAME>.github.io/<REPO_NAME>/,
   * for example your repository is at https://github.com/arifszn/portfolio, then set base to '/portfolio/'.
   */
  base: '/',
  projects: {
    github: {
      display: true, // Display GitHub projects?
      header: 'Github Projects',
      mode: 'automatic', // Mode can be: 'automatic' or 'manual'
      automatic: {
        sortBy: 'stars', // Sort projects by 'stars' or 'updated'
        limit: 8, // How many projects to display.
        exclude: {
          forks: false, // Forked projects will not be displayed if set to true.
          projects: [], // These projects will not be displayed. example: ['arifszn/my-project1', 'arifszn/my-project2']
        },
      },
      manual: {
        // Properties for manually specifying projects
        projects: ['mrdebugger/bs2json', 'mrdebugger/jsoup', 'mrdebugger/nested_inside', 'mrdebugger/alienx', 'mrdebugger/messenger'], // List of repository names to display. example: ['arifszn/my-project1', 'arifszn/my-project2']
      },
    },
    external: {
      header: 'My Projects',
      // To hide the `External Projects` section, keep it empty.
      projects: [
      ],
    },
  },
  seo: {
    title: 'Ijaz Ur Rahim',
    description: 'A passionate Programmer and Security Researcher 🔒.',
    imageURL: 'https://ijazurrahim.com/images/profile.jpg',
  },
  social: {
    linkedin: 'misterdebugger',
    twitter: 'misterdebugger',
    mastodon: '',
    researchGate: '',
    facebook: 'misterdebugger',
    instagram: 'misterdebugger',
    reddit: 'Fragrant_Tea959',
    threads: 'misterdebugger',
    youtube: 'ijazurrahim', // example: 'pewdiepie'
    udemy: 'ijaz-ur-rahim',
    dribbble: '',
    behance: 'ijazurrahim',
    medium: 'mrdebugger',
    dev: '',
    stackoverflow: '9140224/ijaz-ur-rahim', // example: '1/jeff-atwood'
    skype: 'ijazurrahim99',
    telegram: 'misterdebugger',
    website: 'https://ijazurrahim.com',
    phone: '',
    email: 'ijazkhan095@gmail.com',
  },
  resume: {
    fileUrl:
      '', // Empty fileUrl will hide the `Download Resume` button.
  },
  skills: [
    'PHP',
    'JavaScript',
    'React.js',
    'Node.js',
    'Next.js',
    'MySQL',
    'PostgreSQL',
    'Git',
    'Docker',
    'CSS',
    'Python',
    'Django',
    'Flask',
    'Automation',
    'Reverse Engineering'
  ],
  experiences: [
    {
      company: 'Lobstr.io',
      position: 'Sr. Python Engineer',
      from: 'March 2021',
      to: 'Present',
      companyLink: 'https://lobstr.io',
    },
    {
      company: 'Upwork',
      position: 'Freelancer',
      from: 'February 2019',
      to: 'Present',
      companyLink: 'https://upwork.com',
    },
  ],
  certifications: [
  ],
  educations: [
    {
      institution: 'Virtual University Of Pakistan',
      degree: 'Computer engineering',
      from: '2024',
      to: '2027 (expected)',
    },
    {
      institution: 'Abasyn University',
      degree: 'Computer engineering',
      from: '2018',
      to: '2021',
    },
    {
      institution: 'National Institute of Basic Science',
      degree: 'Computer science',
      from: '2016',
      to: '2018',
    },
    {
      institution: 'Imperial College of Engineering Literacy',
      degree: 'Computer science',
      from: '2016',
      to: '2017',
    },
    {
      institution: 'Al-Khalid Public School Shabqadar',
      degree: 'Computer science',
      from: '2009',
      to: '2016',
    },
  ],
  publications: [
  ],
  // Display articles from your medium or dev account. (Optional)
  blog: {
    source: 'medium', // medium | dev
    username: 'mrdebugger', // to hide blog section, keep it empty
    limit: 10, // How many articles to display. Max is 10.
  },
  googleAnalytics: {
    id: '', // GA3 tracking id/GA4 tag id UA-XXXXXXXXX-X | G-XXXXXXXXXX
  },
  // Track visitor interaction and behavior. https://www.hotjar.com
  hotjar: {
    id: '',
    snippetVersion: 6,
  },
  themeConfig: {
    defaultTheme: 'night',

    // Hides the switch in the navbar
    // Useful if you want to support a single color mode
    disableSwitch: false,

    // Should use the prefers-color-scheme media-query,
    // using user system preferences, instead of the hardcoded defaultTheme
    respectPrefersColorScheme: false,

    // Display the ring in Profile picture
    displayAvatarRing: true,

    // Available themes. To remove any theme, exclude from here.
    themes: [
      'light',
      'dark',
      'cupcake',
      'bumblebee',
      'emerald',
      'corporate',
      'synthwave',
      'retro',
      'cyberpunk',
      'valentine',
      'halloween',
      'garden',
      'forest',
      'aqua',
      'lofi',
      'pastel',
      'fantasy',
      'wireframe',
      'black',
      'luxury',
      'dracula',
      'cmyk',
      'autumn',
      'business',
      'acid',
      'lemonade',
      'night',
      'coffee',
      'winter',
      'dim',
      'nord',
      'sunset',
      'procyon',
    ],

    // Custom theme, applied to `procyon` theme
    customTheme: {
      primary: '#fc055b',
      secondary: '#219aaf',
      accent: '#e8d03a',
      neutral: '#2A2730',
      'base-100': '#E3E3ED',
      '--rounded-box': '3rem',
      '--rounded-btn': '3rem',
    },
  },

  // Optional Footer. Supports plain text or HTML.
  footer: `Made with <a 
      class="text-primary" href="https://github.com/arifszn/gitprofile"
      target="_blank"
      rel="noreferrer"
    >GitProfile</a> and ❤️`,

  enablePWA: true,
};

export default CONFIG;
