import "./styles/Career.css";

const Career = () => {
  return (
    <div className="career-section section-container">
      <div className="career-container">
        <h2>
          My career <span>&</span>
          <br /> experience
        </h2>
        <div className="career-info">
          <div className="career-timeline">
            <div className="career-dot"></div>
          </div>
          <div className="career-info-box">
            <div className="career-info-in">
              <div className="career-role">
                <h4>Early Journey</h4>
                <h5>Self-Taught</h5>
              </div>
              <h3>Started</h3>
            </div>
            <p>
              Started building early web projects and automation tools.
            </p>
          </div>
          <div className="career-info-box">
            <div className="career-info-in">
              <div className="career-role">
                <h4>MCA Student</h4>
                <h5>Jagran College, Kanpur</h5>
              </div>
              <h3>Pursuing</h3>
            </div>
            <p>
              Focused on building real products and learning AI. Showcasing apps, tools, and AI projects.
            </p>
          </div>
          <div className="career-info-box">
            <div className="career-info-in">
              <div className="career-role">
                <h4>Full-Stack Developer</h4>
                <h5>Fireflies Infotech Pvt Ltd</h5>
              </div>
              <h3>2024-NOW</h3>
            </div>
            <p>
              Working as a Full-Stack Developer handling Frontend and Backend. Tech Stack includes PHP, Node.js, MySQL, HTML, CSS, JS, Tailwind, Nginx, Docker, and AI Agents (ChatGPT, Gemini, Claude, Grok).
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Career;
