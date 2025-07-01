import Link from "next/link";
import React from "react";
import { BreadcrumbProps } from "@/types/product";

const Breadcrumb: React.FC<BreadcrumbProps> = ({ title, pages }) => {
  return (
    <div className="overflow-hidden shadow-breadcrumb pt-[209px] sm:pt-[155px] lg:pt-[95px] xl:pt-[165px] bg-gradient-to-r from-orange-100 via-yellow-100 to-green-100">
      <div className="border-t-4 border-gradient-to-r border-orange-400">
        <div className="max-w-[1170px] w-full mx-auto px-4 sm:px-8 xl:px-0 py-5 xl:py-10">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <h1 className="font-semibold text-gray-800 text-xl sm:text-2xl xl:text-custom-2 bg-white px-4 py-2 rounded-lg shadow-md border-l-4 border-orange-500">
              {title}
            </h1>

            <ul className="flex items-center gap-2 bg-white px-3 py-2 rounded-lg shadow-sm">
              <li className="text-custom-sm hover:text-orange-600 transition-colors">
                <Link href="/">Inicio /</Link>
              </li>

              {pages.length > 0 &&
                pages.map((page, key) => (
                  <li className="text-custom-sm last:text-green-600 last:font-medium capitalize" key={key}>
                    {page} 
                  </li>
                ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Breadcrumb;
