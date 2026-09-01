import "./Home.css";

import {CURRENT_USER} from "../../features/user";
import {PROGRESS_METRICS} from "../../features/progress";
import {RecordingQuickActions, ProgressCard} from "../../components";

/**
 * The Home Page for Notes Gen AI
 *
 * @constructor constructure for home page
 *
 * @author Yubraj Sahoo
 */
export const Home = () => {
    return (
        <>
            <div className={`page-container`}>
                <div style={{marginBottom: 'var(--margin-2)'}}>
                    <h4>
                        {CURRENT_USER.greetings}, {CURRENT_USER.name} <span role="img" aria-label="wave">👋</span>
                    </h4>
                    <p className={`text-secondary`}>
                        What would you like to learn today?
                    </p>
                </div>

                <div className="home-top-section">
                    <div className="home-top-left">
                        <RecordingQuickActions/>
                    </div>
                    <div className="home-top-right">
                        <ProgressCard metrics={PROGRESS_METRICS}/>
                    </div>
                </div>
            </div>
        </>
    );
};
