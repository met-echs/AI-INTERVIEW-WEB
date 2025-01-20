import React from "react";
import web from "../src/images/interviews-e.jpg";
import { NavLink } from "react-router-dom";

const Home = () => {
  return (
    <section id="header" className="d-flex align-items-center">
      <div className="container-fluid">
        <div className="row">
          <div className="col-10 mx-auto">
            <div className="row">
              <div className="col-md-6 pt-5 pt-lg-0 order-2 order-lg-1 d-flex justify-content-center flex-column">
                <h1>
                  Today's decision is tommorow's victory <strong className="brand-name">Build your life</strong>
                </h1>
                <h2 className="my-3">
                  Make a better future by selecting a good path
                </h2>
                <div className="mt-3">
                  <NavLink to="/Apply" className="btn-get-started">
                    APPLY NOW
                  </NavLink>
                </div>
                <p style={{ color: "#333", lineHeight: "1.6", padding: "20px 0" }}>
                  <strong>Job Description:</strong> We are seeking a talented <b>FULL STACK DEVOLOPER </b>
                  to design, develop, and maintain scalable web applications.
                  The ideal candidate will have a strong understanding of both front-end
                  and back-end development, as well as a passion for building
                  high-performance, user-friendly solutions.
                </p>
              </div>
              <div className="col-lg-6 order-1 order-lg-2 header-img">
                <img src={web} className="img-fluid animated" alt="home img" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Home;