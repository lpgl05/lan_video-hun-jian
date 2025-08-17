import React from 'react';

import styles from './index.module.scss';

const Component = () => {
  return (
    <div className={styles.bRixAgency}>
      <div className={styles.wrapper}>
        <div className={styles.background}>
          <div className={styles.illustration} />
        </div>
        <div className={styles.a40Px}>
          <div className={styles.a28Px}>
            <img src="../image/mef2stg5-d3syp4h.svg" className={styles.logo} />
            <div className={styles.a14Px}>
              <p className={styles.title}>
                Looking to design & develop
                <br />
                an amazing website?
              </p>
              <p className={styles.paragraph}>
                Need a hand to design and develop a world-class website for your
                company, or to create a premium UI/UX design for your app? <br />
                At BRIX Agency we are ready to help you!
              </p>
            </div>
          </div>
          <div className={styles.primaryBtn}>
            <p className={styles.buttonText}>Get in touch</p>
            <img src="../image/mef2stg5-9wze54l.svg" className={styles.icon} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Component;
