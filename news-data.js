/**
 * News Data File
 * 这个文件包含所有的新闻数据
 * 可以随时更新，最新的三条新闻会自动显示在首页的 "Recent Breakthroughs" 区
 */

const NEWS_DATA = [
  {
    id: 1,
    date: "June, 2026",
    category: "Xiamen University",
    title: "Academician Xiao Wei Sun visits Academician Hu Wenping, President of Xiamen University",
    summary: "Recently, Xiao Wei Sun, foreign academician of the Russian Academy of Sciences, the executive dean of the Institute of Nanoscience and Application of the SUST, and the chair professor of the Department of Electrical and Electronic Engineering, visited Academician Hu Wenping, President of Xiamen University.",
    body: "<p>Recently, Xiao Wei Sun, foreign academician of the Russian Academy of Sciences, the executive dean of the Institute of Nanoscience and Application of the SUST, and the chair professor of the Department of Electrical and Electronic Engineering, visited Academician Hu Wenping, President of Xiamen University.</p><p>During the visit, both sides engaged in in-depth exchanges on cutting-edge research in nanoscience and display technology, and explored potential collaboration opportunities between the two institutions. The meeting underscored the importance of inter-university cooperation in advancing frontier science and technology.</p><p>Academician Sun and President Hu discussed joint research initiatives, student exchange programs, and the possibility of co-organizing international symposia. Both parties expressed strong willingness to deepen ties and create a lasting partnership for mutual benefit.</p>",
    media: {
      type: "image",
      src: "10.jpg",
      alt: "Xiamen University Visit"
    }
  },
  {
    id: 2,
    date: "May, 2026",
    category: "Nature",
    title: "Academician Xiao Wei Sun's team was invited to publish a research review article in Nature",
    summary: "Recently, at the invitation of the top academic journal Nature, Xiao Wei Sun published a research review article titled \"Glasses free display switches between 2D and 3D\" in the Nature News & Views section.",
    body: "<p>Recently, at the invitation of the top academic journal Nature, Xiao Wei Sun published a research review article titled \"Glasses free display switches between 2D and 3D\" in the Nature News &amp; Views section.</p><p>The article provides an in-depth analysis of the latest advances in autostereoscopic display technology, examining the underlying physical principles that enable seamless switching between conventional 2D and immersive 3D viewing modes without the need for special eyewear.</p><p>This invitation-only contribution reflects the international recognition of Sun Lab's leading position in the field of advanced display research. The review is expected to guide future research directions and inspire new approaches to glasses-free 3D display development worldwide.</p>",
    media: {
      type: "image",
      src: "9.jpg",
      alt: "Nature Review"
    }
  },
  {
    id: 3,
    date: "May, 2026",
    category: "Shenzhen News",
    title: "Exclusive interview on Huawei's \"Tao Law\"",
    summary: "Shenzhen News conducted an exclusive interview with Xiao Wei Sun, Executive Dean of the Institute of Nano Science and Applications at the Southern University of Science and Technology, discussing the implications of Huawei's \"Tao Law\" for the semiconductor and display industries.",
    body: "<p>Shenzhen News conducted an exclusive interview with Xiao Wei Sun, Executive Dean of the Institute of Nano Science and Applications at the Southern University of Science and Technology, discussing the implications of Huawei's \"Tao Law\" for the semiconductor and display industries.</p><p>In the interview, Academician Sun offered his expert perspective on how rapid advances in chip architecture and photonics are reshaping the competitive landscape for global technology companies. He emphasized that China's homegrown innovation capabilities have reached a critical inflection point.</p><p>Academician Sun also highlighted Sun Lab's ongoing research into next-generation display drivers and photonic integration, noting that collaborative efforts between academia and industry will be essential to sustaining long-term technological leadership.</p>",
    media: {
      type: "video",
      src: "1.mp4",
      alt: "Interview Video"
    }
  },
  {
    id: 4,
    date: "April, 2026",
    category: "Research",
    title: "Breakthrough in Quantum Dot Technology",
    summary: "Our team has achieved a major breakthrough in quantum dot efficiency, increasing the luminescence by 35% compared to previous generations.",
    body: "<p>Our team has achieved a major breakthrough in quantum dot efficiency, increasing the luminescence by 35% compared to previous generations. This result was obtained through a novel surface passivation technique that significantly reduces non-radiative recombination at the quantum dot interface.</p><p>The new approach involves a carefully engineered ligand exchange process that stabilizes the quantum dot surface while maintaining optimal charge carrier injection. This dual benefit simultaneously improves brightness and extends operational lifetime.</p><p>The findings have been submitted for peer review and are expected to accelerate the development of next-generation quantum dot LED displays with superior color purity and energy efficiency.</p>",
    media: {
      type: "image",
      src: "research-01.jpg",
      alt: "Quantum Dot Research"
    }
  },
  {
    id: 5,
    date: "March, 2026",
    category: "Conference",
    title: "International AR Display Conference Participation",
    summary: "The team presented latest findings on AR waveguide display technology at the International Conference on Advanced Displays.",
    body: "<p>The team presented latest findings on AR waveguide display technology at the International Conference on Advanced Displays, attracting significant attention from industry leaders and academic peers worldwide.</p><p>The presentation covered Sun Lab's proprietary diffractive waveguide architecture, which achieves a record-high field of view while maintaining compact form factor suitable for consumer wearable devices. The work was recognized with a Best Paper Award nomination at the conference.</p><p>Following the presentation, several collaborative research proposals were initiated with partner institutions from Europe and North America, setting the stage for joint publications and technology transfer opportunities in the near future.</p>",
    media: {
      type: "image",
      src: "conference-01.jpg",
      alt: "Conference Presentation"
    }
  }
];
