import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

function mapApiError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;

    if (error.response?.status === 502) {
      return new Error('Backend is temporarily overloaded. Please wait 20-30 seconds and try again with a smaller PDF.');
    }

    if (typeof detail === 'string' && detail.trim()) {
      return new Error(detail);
    }

    const rawMessage = String(error.message || '').toLowerCase();
    if (rawMessage.includes('err_blocked_by_client') || rawMessage.includes('blocked by client')) {
      return new Error('Request blocked by browser extension/privacy shield. Disable ad-block/privacy shield for this site and retry.');
    }

    if (error.code === 'ERR_NETWORK') {
      return new Error('Network error while contacting backend. Check connection and retry.');
    }
  }

  if (error instanceof Error) {
    return error;
  }

  return new Error('Unexpected error while contacting backend.');
}

export const uploadPaper = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 180000,
    });
    return response.data;
  } catch (error) {
    throw mapApiError(error);
  }
};

export const analyzePaper = async (paperId: string) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/analyze`,
      { paper_id: paperId },
      { timeout: 180000 }
    );
    return response.data;
  } catch (error) {
    throw mapApiError(error);
  }
};
