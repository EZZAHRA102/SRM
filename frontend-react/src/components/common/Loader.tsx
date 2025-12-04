import { motion } from 'framer-motion';

export const Loader = () => {
  return (
    <div className="flex items-center justify-center gap-2">
      <motion.div
        className="w-4 h-4 bg-srm-green border-2 border-srm-black"
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 90, 180],
          borderRadius: ["0%", "20%", "0%"]
        }}
        transition={{
          duration: 1.5,
          ease: "easeInOut",
          repeat: Infinity,
          delay: 0
        }}
      />
      <motion.div
        className="w-4 h-4 bg-srm-blue border-2 border-srm-black"
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 90, 180],
          borderRadius: ["0%", "20%", "0%"]
        }}
        transition={{
          duration: 1.5,
          ease: "easeInOut",
          repeat: Infinity,
          delay: 0.2
        }}
      />
      <motion.div
        className="w-4 h-4 bg-srm-orange border-2 border-srm-black"
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 90, 180],
          borderRadius: ["0%", "20%", "0%"]
        }}
        transition={{
          duration: 1.5,
          ease: "easeInOut",
          repeat: Infinity,
          delay: 0.4
        }}
      />
    </div>
  );
};

