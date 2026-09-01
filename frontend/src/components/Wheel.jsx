import { useEffect, useState } from "react";

/**
 * The backend already picked the winner (result) - this animates through
 * candidate titles with easing (fast -> slow) before landing on it, plus
 * a blur/glow effect while spinning for more visual weight.
 */
export default function Wheel({ candidates, result, onFinished }) {
  const [displayTitle, setDisplayTitle] = useState(candidates[0]?.title || "");
  const [spinning, setSpinning] = useState(true);
  const [tickCount, setTickCount] = useState(0);

  useEffect(() => {
    let tick = 0;
    const totalTicks = 22;
    let timeoutId;

    function scheduleNext() {
      tick += 1;
      setTickCount(tick);

      if (tick >= totalTicks) {
        setDisplayTitle(result.title);
        setSpinning(false);
        setTimeout(onFinished, 900);
        return;
      }

      const pool = candidates.map((c) => c.title);
      const randomIndex = Math.floor(Math.random() * pool.length);
      setDisplayTitle(pool[randomIndex]);

      // ease out: delay grows quadratically as we approach the end
      const progress = tick / totalTicks;
      const delay = 70 + Math.pow(progress, 2) * 260;
      timeoutId = setTimeout(scheduleNext, delay);
    }

    timeoutId = setTimeout(scheduleNext, 70);

    return () => clearTimeout(timeoutId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const blurAmount = spinning ? Math.max(0, 2 - (tickCount / 22) * 2) : 0;

  return (
    <div className="pixel-panel wheel-stage">
      <div className="section-heading">
        {spinning ? "Spinning..." : "Landed on:"}
      </div>
      <div className={`wheel-scroll-window ${spinning ? "wheel-spinning" : "wheel-landed"}`}>
        <div
          className="wheel-title"
          style={{ filter: `blur(${blurAmount}px)` }}
        >
          {displayTitle}
        </div>
      </div>
    </div>
  );
}