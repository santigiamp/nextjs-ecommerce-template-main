import React, { useState, useEffect, useRef } from "react";
import { CustomSelectProps, SelectOption } from "@/types/product";

const CustomSelect: React.FC<CustomSelectProps> = ({ options }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState(options[0]);
  const selectRef = useRef<HTMLDivElement>(null);

  // Function to close the dropdown when a click occurs outside the component
  const handleClickOutside = (event: MouseEvent) => {
    if (selectRef.current && event.target && !selectRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    // Add a click event listener to the document
    document.addEventListener("click", handleClickOutside);

    // Clean up the event listener when the component unmounts
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option: SelectOption) => {
    setSelectedOption(option);
    toggleDropdown();
  };

  return (
    <div
      className="custom-select custom-select-2 flex-shrink-0 relative"
      ref={selectRef}
    >
      <div
        className={`select-selected whitespace-nowrap bg-gradient-to-r from-green-100 to-blue-100 border-2 border-green-300 rounded-lg px-3 py-2 cursor-pointer hover:from-green-200 hover:to-blue-200 transition-all ${
          isOpen ? "select-arrow-active" : ""
        }`}
        onClick={toggleDropdown}
      >
        {selectedOption.label}
      </div>
      <div className={`select-items bg-white border-2 border-green-300 rounded-lg shadow-lg mt-1 ${isOpen ? "block" : "hidden"}`}>
        {options.slice(1).map((option, index) => (
          <div
            key={index}
            onClick={() => handleOptionClick(option)}
            className={`select-item px-3 py-2 cursor-pointer hover:bg-gradient-to-r hover:from-yellow-100 hover:to-orange-100 transition-all ${
              selectedOption === option ? "bg-gradient-to-r from-green-200 to-blue-200 font-medium" : ""
            }`}
          >
            {option.label}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CustomSelect;
