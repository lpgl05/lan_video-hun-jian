import React from 'react';

import styles from './index.module.scss';

const Component = () => {
  return (
    <div className={styles.bRixTemplates}>
      <div className={styles.wrapper}>
        <div className={styles.background}>
          <div className={styles.a40Px}>
            <div className={styles.a28Px}>
              <img src="../image/mef43jv9-m0nyvfx.svg" className={styles.logo} />
              <div className={styles.a14Px}>
                <p className={styles.title}>
                  Looking for an amazing Webflow Template for your website?
                </p>
                <p className={styles.paragraph}>
                  We don't just have great Figma freebies, we also design & develop
                  the best Webflow Templates out there!
                </p>
              </div>
            </div>
            <div className={styles.primaryBtn}>
              <p className={styles.buttonText}>Browse templates</p>
              <img src="../image/mef43jv9-uoa9vaz.svg" className={styles.icon} />
            </div>
          </div>
        </div>
        <img src="../image/mef43jv9-04cbyky.png" className={styles.illustration} />
      </div>
    </div>
  );
}

export default Component;
