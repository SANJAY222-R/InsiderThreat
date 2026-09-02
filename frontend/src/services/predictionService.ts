/**
 * Prediction Service
 *
 * API calls for threat predictions.
 *
 * Phase 0: Stub only.
 */

export const predictionService = {
  async predict(_employeeId: string) {
    throw new Error("Not implemented");
  },

  async batchPredict(_employeeIds: string[]) {
    throw new Error("Not implemented");
  },

  async getResult(_predictionId: number) {
    throw new Error("Not implemented");
  },
};
