import React from "react";
import ReactDOM from "react-dom";
import "./index.scss";

interface ModalProps {
  children?: React.ReactNode;
  isOpen: boolean;
  onClose?: () => void;
  title: string;
  width?: number;
  height?: number | string;
  showHeader?: boolean;
  showFooter?: boolean;
}

const ModalContent = ({
  children,
  isOpen,
  onClose,
  title,
  width = 500,
  height = 500,
  showHeader = true,
  showFooter = true,
}: ModalProps) => {
  return (
    <div
      className="modal"
      style={{
        display: isOpen ? "flex" : "none",
        transform: isOpen ? "translateY(0)" : "translateY(-100%)",
      }}
    >
      <div className="modal-content" style={{ width, height }}>
        {showHeader && (
          <div className="modal-header">
            <div className="modal-title">{title}</div>
            <button onClick={onClose} className="modal-close-btn">
              Close
            </button>
          </div>
        )}
        <div className="modal-children">{children}</div>
        {showFooter && (
          <div className="modal-footer">
            <button className="modal-footer-btn no" onClick={onClose}>
              Cancel
            </button>
            <button className="modal-footer-btn yes">Next</button>
          </div>
        )}
      </div>
    </div>
  );
};

const ModalPortal = ({ children }: any) => {
  const modalRoot = document.getElementById("modal-root");

  return ReactDOM.createPortal(children, modalRoot || document.body);
};

const Modal = (props: ModalProps) => {
  return (
    <ModalPortal>
      <ModalContent {...props} />
    </ModalPortal>
  );
};

export default Modal;
