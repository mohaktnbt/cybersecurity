import { create } from "zustand";

interface Scan {
  id: string;
  targetId: string;
  status: string;
  scanType: string;
  createdAt: string;
}

interface ScanStore {
  scans: Scan[];
  activeScan: Scan | null;
  setScans: (scans: Scan[]) => void;
  setActiveScan: (scan: Scan | null) => void;
}

export const useScanStore = create<ScanStore>((set) => ({
  scans: [],
  activeScan: null,
  setScans: (scans) => set({ scans }),
  setActiveScan: (scan) => set({ activeScan: scan }),
}));
