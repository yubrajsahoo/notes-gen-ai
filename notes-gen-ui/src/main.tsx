import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
// 1. Third-party styles and scripts FIRST
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// 2. Global custom styles SECOND
import './styles/variables.css'
import './index.css'

import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <App/>
    </StrictMode>,
)
