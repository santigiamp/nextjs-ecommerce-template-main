// EmailJS Configuration
export const EMAILJS_CONFIG = {
  SERVICE_ID: 'service_kdoe2nj',
  TEMPLATE_ID: 'template_aljkuql', 
  PUBLIC_KEY: 'RPSv8h7q8u2nvcTXW'
};

export interface EmailParams {
  from_name: string;
  from_email: string;
  phone: string;
  product: string;
  quantity: string;
  comments: string;
  order_date: string;
}