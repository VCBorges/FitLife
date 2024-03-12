import React from "react";
import { LogoutForm } from "./forms/LogoutForm";
import { FitLifeLogo } from "./FitLifeLogo";

import '../styles/navBar.css';

export function NavBar({
    logoutEndpoint,
    fitLifeLogo,
}) {
    return (
        <nav 
            className="navbar navbar-dark bg-dark" 
            aria-label="Dark offcanvas navbar"
        >
            <div className="container-fluid navbar-body">
                <a className="navbar-brand" href="#">
                    <FitLifeLogo 
                        fitLifeLogo={fitLifeLogo}
                    />
                </a>
                
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasNavbarDark"
                    aria-controls="offcanvasNavbarDark"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon" />
                </button>
                <div
                    className="offcanvas offcanvas-start text-bg-dark"
                    tabIndex={-1}
                    id="offcanvasNavbarDark"
                    aria-labelledby="offcanvasNavbarDarkLabel"
                >
                    <div className="offcanvas-header">
                        <h5 className="offcanvas-title" id="offcanvasNavbarDarkLabel">
                            <FitLifeLogo 
                                fitLifeLogo={fitLifeLogo}
                            />
                        </h5>
                        <button
                            type="button"
                            className="btn-close btn-close-white"
                            data-bs-dismiss="offcanvas"
                            aria-label="Close"
                        />
                    </div>
                    <div className="offcanvas-body">
                        <ul className="navbar-nav justify-content-end flex-grow-1 pe-3">
                            <li className="nav-item">
                                <a className="nav-link active" aria-current="page" href="#">
                                    Home
                                </a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="#">
                                    Link
                                </a>
                            </li>
                            <li className="nav-item dropdown">
                                <a
                                    className="nav-link dropdown-toggle"
                                    href="#"
                                    role="button"
                                    data-bs-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                    Dropdown
                                </a>
                                <ul className="dropdown-menu">
                                    <li>
                                        <a className="dropdown-item" href="#">
                                            Action
                                        </a>
                                    </li>
                                    <li>
                                        <a className="dropdown-item" href="#">
                                            Another action
                                        </a>
                                    </li>
                                    <li>
                                        <hr className="dropdown-divider" />
                                    </li>
                                    <li>
                                        <a className="dropdown-item" href="#">
                                            Something else here
                                        </a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                        <form className="d-flex mt-3" role="search">
                            <input
                                className="form-control me-2"
                                type="search"
                                placeholder="Search"
                                aria-label="Search"
                            />
                            <button className="btn btn-outline-success" type="submit">
                                Search
                            </button>
                        </form>
                    </div>
                </div>
                <div className="ms-auto">
                    <LogoutForm
                        logoutEndpoint={logoutEndpoint}
                    />
                </div>
            </div>
        </nav>
    );
}