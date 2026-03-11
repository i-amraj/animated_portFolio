import "./styles/Work.css";
import WorkImage from "./WorkImage";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

const projects = [
  {
    name: "Library Management",
    category: "Full-Stack Web App",
    tools: "Laravel, MySQL, PHP",
    image: "/images/library.png",
  },
  {
    name: "YT Checker",
    category: "AI Analysis Tool",
    tools: "Node.js, YouTube API, Gemini AI",
    image: "/images/yt-checker.png",
  },
  {
    name: "Leads Generator",
    category: "Automation Scraper",
    tools: "Node.js, Playwright, Express",
    image: "/images/raj-leads.png",
  },
  {
    name: "Music App",
    category: "Mobile App",
    tools: "Flutter, Dart, Provider",
    image: "/images/raj-music.jpeg",
  },
  {
    name: "Health AI Assistant",
    category: "AI Health Assistant",
    tools: "PHP, Laravel, Gemini AI, MySQL",
    image: "/images/health-ai.png",
  },
];

const Work = () => {
  useGSAP(() => {
    let translateX: number = 0;

    function setTranslateX() {
      const box = document.getElementsByClassName("work-box");
      const rectLeft = document
        .querySelector(".work-container")!
        .getBoundingClientRect().left;
      const rect = box[0].getBoundingClientRect();
      const parentWidth = box[0].parentElement!.getBoundingClientRect().width;
      let padding: number =
        parseInt(window.getComputedStyle(box[0]).padding) / 2;
      translateX = rect.width * box.length - (rectLeft + parentWidth) + padding;
    }

    setTranslateX();

    let timeline = gsap.timeline({
      scrollTrigger: {
        trigger: ".work-section",
        start: "top top",
        end: `+=${translateX}`, // Use actual scroll width
        scrub: true,
        pin: true,
        id: "work",
      },
    });

    timeline.to(".work-flex", {
      x: -translateX,
      ease: "none",
    });

    // Clean up (optional, good practice)
    return () => {
      timeline.kill();
      ScrollTrigger.getById("work")?.kill();
    };
  }, []);
  return (
    <div className="work-section" id="work">
      <div className="work-container section-container">
        <h2>
          My <span>Work</span>
        </h2>
        <div className="work-flex">
          {projects.map((project, index) => (
            <div className="work-box" key={index}>
              <div className="work-info">
                <div className="work-title">
                  <h3>0{index + 1}</h3>

                  <div>
                    <h4>{project.name}</h4>
                    <p>{project.category}</p>
                  </div>
                </div>
                <h4>Tools and features</h4>
                <p>{project.tools}</p>
              </div>
              <WorkImage image={project.image} alt="" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Work;
