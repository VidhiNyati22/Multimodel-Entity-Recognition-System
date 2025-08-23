// import React from 'react';
// import { render, screen, fireEvent, waitFor } from '@testing-library/react';
// import { BrowserRouter } from 'react-router-dom';
// import Home from './home';

// test('renders Home component', () => {
//   render(
//     <BrowserRouter>
//       <Home />
//     </BrowserRouter>
//   );
//   expect(screen.getByText(/Enter Text Here/i)).toBeInTheDocument();
// });

// test('handles input change', () => {
//   render(
//     <BrowserRouter>
//       <Home />
//     </BrowserRouter>
//   );
//   const input = screen.getByPlaceholderText(/Enter your text here/i);
//   expect(input).toBeInTheDocument();

//   fireEvent.change(input, { target: { value: 'Test input' } });
//   expect(input.value).toBe('Test input');
// });

// test('handles model selection', () => {
//   render(
//     <BrowserRouter>
//       <Home />
//     </BrowserRouter>
//   );
//   const select = screen.getByRole('combobox');
//   expect(select).toBeInTheDocument();

//   fireEvent.change(select, { target: { value: 'model1' } });
//   expect(select.value).toBe('model1');
// });

// test('disables button when input or model is not selected', () => {
//   render(
//     <BrowserRouter>
//       <Home />
//     </BrowserRouter>
//   );
//   const button = screen.getByRole('button', { name: /Get Output/i });
//   expect(button).toBeInTheDocument();
//   expect(button).toBeDisabled();
// });

// // Add more tests as needed