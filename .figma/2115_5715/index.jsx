import React from 'react';

import styles from './index.module.scss';

const Component = () => {
  return (
    <div className={styles.thanksForDownloading}>
      <img src="../image/mef2tzx1-hquhy86.png" className={styles.background2} />
      <div className={styles.wrapper2}>
        <img src="../image/mef2tzx1-r2mgco9.png" className={styles.illustration} />
        <div className={styles.a40Px}>
          <div className={styles.wrapper}>
            <div className={styles.heartIcon} />
            <div className={styles.a14Px}>
              <p className={styles.title}>
                Thanks for downloading our Figma cloneable.
              </p>
              <p className={styles.paragraph5}>
                <span className={styles.paragraph}>
                  Thanks for downloading our&nbsp;
                </span>
                <span className={styles.paragraph2}>Multi-step Form</span>
                <span className={styles.paragraph}>
                  , we hope it is useful for you. If you are looking for more
                  amazing free Figma Templates, we recommend you to follow us in
                  the&nbsp;
                </span>
                <span className={styles.paragraph3}>Figma Community</span>
                <span className={styles.paragraph4}>.</span>
              </p>
            </div>
          </div>
          <div className={styles.primaryBtn}>
            <p className={styles.buttonText}>Follow us</p>
            <img src="../image/mef2tzx1-hg1aojj.svg" className={styles.icon} />
          </div>
        </div>
        <div className={styles.figmaLogo} />
      </div>
    </div>
  );
}

export default Component;
